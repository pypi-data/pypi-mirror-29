=======
History
=======

0.1.2 (Current version)
-----------------------

API changes
~~~~~~~~~~~

* :py:func:`impax.csvv.get_gammas` has been deprecated. Use :py:func:`impax.read_csvv` instead (:issue:`37`)
* :py:meth:`~impax.csvv.Gammas._prep_gammas` has been removed, and :py:meth:`~impax.csvv.Gammas.sample` now
  takes no arguments and returns a sample by default. Seeding the random number generator is now left up to
  the user (:issue:`36`)


Bug fixes
~~~~~~~~~

* fix py3k compatability issues (:issue:`39`)
* fix travis status icon in README
* add tests for :py:func:`impax.mins._minimize_polynomial`, fix major math errors causing a failure to find minima in :py:mod:`impax.mins` module, and clarify documentation (:issue:`58`)


0.1.0 (2017-10-12)
------------------

* First release on PyPI.
