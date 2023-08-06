from __future__ import absolute_import
import os
import xarray as xr
import pandas as pd
import numpy as np
from impax.mins import minimize_polynomial


def construct_weather(**weather):
    '''
    Helper function to build out weather dataarray

    Parameters
    ----------

    weather: dict
        dictionary of prednames and weather (either ``str`` file paths
        or :py:class:`xarray.DataArray` objects) for each predname

    Returns
    -------
    combined: DataArray
            Combined :py:class:`~xarray.DataArray` of weather
            variables, with variables concatenated along the
            new `prednames` dimension

    '''
    prednames = []
    weather_data = []
    for pred, path in weather.items():
        if hasattr(path, 'dims'):
            weather_data.append(path)

        else:
            with xr.open_dataset(path) as ds:
                weather_data.append(ds[pred].load())

        prednames.append(pred)

    return xr.concat(weather_data, pd.Index(prednames, name='prednames'))


def construct_covars(add_constant=True, **covars):
    '''
    Helper function to construct the covariates dataarray

    Parameters
    -----------
    add_constant : bool
        flag indicating whether a constant term should be added. The constant
        term will have the same shape as the other covariate DataArrays

    covars: dict
        dictionary of covariate name, covariate (``str`` path or
        :py:class:`xarray.DataArray`) pairs

    Returns
    -------
    combined: DataArray
        Combined :py:class:`~xarray.DataArray` of covariate
        variables, with variables concatenated along the
        new `covarnames` dimension
    '''
    covarnames = []
    covar_data = []
    for covar, path in covars.items():
        if hasattr(path, 'dims'):
            covar_data.append(path)

        else:
            with xr.open_dataset(path) as ds:
                covar_data.append(ds[covar].load())

        covarnames.append(covar)

    if add_constant:
        ones = xr.DataArray(
            np.ones(shape=covar_data[0].shape),
            coords=covar_data[0].coords,
            dims=covar_data[0].dims)
        covarnames.append('1')
        covar_data.append(ones)

    return xr.concat(covar_data, pd.Index(covarnames, name='covarnames'))


class Impact(object):
    '''
    Base class for computing an impact as specified by the Climate Impact Lab

    '''

    min_function = NotImplementedError

    def impact_function(self, betas, weather):
        '''
        computes the dot product of betas and annual weather by outcome group

        Parameters
        ----------

        betas: DataArray
            :py:class:`~xarray.DataArray` of hierid by predname by outcome

        weather: DataArray
            :py:class:`~xarray.DataArray` of hierid by predname by outcome

        Returns
        -------
        DataArray
            :py:class:`~xarray.DataArray` of impact by outcome by hierid

        .. note::

            overrides `impact_function` method in Impact base class

        '''

        return (betas*weather).sum(dim='prednames')

    def compute(
            self,
            weather,
            betas,
            clip_flat_curve=True,
            t_star=None):
        '''
        Computes an impact for a unique set of gdp, climate, weather and gamma
        coefficient inputs. For each set of these, we take the analytic minimum
        value between two points, save t_star to disk and compute analytical
        min for function m_star for a given covariate set.

        This operation is called for every adaptation scenario specified in the
        run script.

        Parameters
        ----------

        weather: DataArray
          weather :py:class:`~xarray.DataArray`

        betas: DataArray
          covarname by outcome :py:class:`~xarray.DataArray`

        clip_flat_curve: bool
          flag indicating that flat-curve clipping should be performed
          on the result

        t_star: DataArray
          :py:class:`xarray.DataArray` with minimum temperatures used for
          clipping


        Returns
        -------
          :py:class `~xarray.Dataset` of impacts by hierid by outcome group

        '''

        # Compute Raw Impact
        impact = self.impact_function(betas, weather)

        if clip_flat_curve:

            # Compute the min for flat curve adaptation
            impact_flatcurve = self.impact_function(betas, t_star)

            # Compare values and evaluate a max
            impact = xr.ufuncs.maximum((impact - impact_flatcurve), 0)

        impact = self.postprocess_daily(impact)

        # Sum to annual
        impact = impact.sum(dim='time')

        impact_annual = self.postprocess_annual(impact)

        return impact_annual

    def get_t_star(self, betas, bounds, t_star_path=None):
        '''
        Read precomputed t_star

        Parameters
        ----------

        betas: DataArray
            :py:class:`~xarray.DataArray` of betas as prednames by hierid

        bounds: list
            values between which to evaluate function

        path: str
          place to load t-star from

        '''

        try:
            with xr.open_dataarray(t_star_path) as t_star:
                return t_star.load()

        except OSError:
            pass

        except (IOError, ValueError):
            try:
                os.remove(t_star_path)
            except (IOError, OSError):
                pass

        # Compute t_star according to min function
        t_star = self.compute_t_star(betas, bounds=bounds)

        # write to disk
        if t_star_path is not None:
            if not os.path.isdir(os.path.dirname(t_star_path)):
                os.makedirs(os.path.dirname(t_star_path))

            t_star.to_netcdf(t_star_path)

        return t_star

    def compute_t_star(self, betas, bounds=None):
        return self.min_function(betas, bounds=bounds)

    def postprocess_daily(self, impact):
        return impact

    def postprocess_annual(self, impact):
        return impact


class PolynomialImpact(Impact):
    '''
    Polynomial-specific Impact spec, with ln(gdppc) and climtas for covariates
    '''

    @staticmethod
    def min_function(*args, **kwargs):
        '''
        helper function to call minimization function for given mortality
        polynomial spec mortality_polynomial implements findpolymin through
        `np.apply_along_axis`

        Parameters
        ----------

        betas: DataArray
            :py:class:`~xarray.DataArray` of hierid by predname by outcome

        dim: str
            dimension to apply minimization to

        bounds: list
            values between which to search for t_star

        Returns
        -------
            :py:class:`~xarray.DataArray` of hierid by predname by outcome

        .. note:: overides `min_function` in Impact base class
        '''

        return minimize_polynomial(*args, **kwargs)
