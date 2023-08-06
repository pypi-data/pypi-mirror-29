Changes\ [#]_
-------------

3.2 (2018-03-03)
~~~~~~~~~~~~~~~~

* Use `python-rapidjson`__ if available

  __ https://pypi.org/project/python-rapidjson/


3.1 (2017-11-30)
~~~~~~~~~~~~~~~~

* Fix glitch in the logic that determine whether a patch script is still valid

* Use enlighten__ to show the progress bar: the ``--verbose`` option is gone, now is the
  default mode

  __ https://pypi.org/project/enlighten/


3.0 (2017-11-06)
~~~~~~~~~~~~~~~~

* Python 3 only\ [#]_

* New execution logic, hopefully fixing circular dependencies error in case of multiple non
  trivial pending migrations


.. [#] Previous changes are here__.

       __ https://bitbucket.org/lele/metapensiero.sphinx.patchdb/src/master/OLDERCHANGES.rst

.. [#] If you are still using Python 2, either stick with version 2.27, or fetch `this
       commit`__ from the repository.

       __ https://bitbucket.org/lele/sol/commits/f9fc5f5d50a381eaf9f003d7006cc46382842c18
