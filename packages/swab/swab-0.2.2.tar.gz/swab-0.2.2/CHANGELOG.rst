
0.2.2 (released 2018-02-23)
---------------------------

* Bugfix: fix for exception triggered when a bot visits a page containing
  ``record_trial_tag``

0.2.1 (released 2018-02-23)
---------------------------

* Bugfix: fixed link rendering on test results page

0.2.0 (released 2018-02-23)
---------------------------

* Compatibility with python 3
* Allow the application to force a variant when calling show_variant
* Improved JS snippet no longer blocks browser rendering
* No longer records duplicate trials if show_variant is called twice
* Allow experiments to customize the swabid generation strategy - useful if
  you want to deterministically seed the RNG based on some request attribute.
* Allow weighted variants: ``add_experiment('foo', 'AAAB')`` will show
  variant A 75% of the time.
* Include bayesian results calculation based on
  http://www.evanmiller.org/bayesian-ab-testing.html#binary_ab_implementation
* Better caching: only sets cookies on pages where an experiment is invoked
* ``record_trial_tag`` can now infer the experiment name from a previous call
  to ``show_variant``: less duplicated code when running an experiment.
* Results now show results per visitor by default

Version 0.1.3
-------------

* Added a javascript beacon to record tests (helps exclude bots)
* Better exclusion of bots on server side too
* Record trial app won't raise an error if the experiment name doesn't exist
* Removed debug flag, the ability to force a variant is now always present
* Strip HTTP caching headers if an experiment has been invoked during the request
* Improved accuracy of conversion tracking
* Cookie path can be specified in middleware configuration

Version 0.1.2
-------------

* Minor bugfixes

Version 0.1.1
-------------

* Bugfix for ZeroDivisionErrors when no data has been collected

Version 0.1
-------------

* Initial release

