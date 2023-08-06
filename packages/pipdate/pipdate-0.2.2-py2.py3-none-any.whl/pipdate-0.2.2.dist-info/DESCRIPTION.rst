pipdate
=======

|CircleCI| |codecov| |Codacy grade| |PyPi Version| |GitHub stars|

pipdate is a collection of small pip update helpers. The commands

::

    pipdate
    pipdate3

updates *all* your pip{3}-installed packages.

There's a Python interface as well that can be used for update
notifications. This

.. code:: python

    import pipdate
    msg = pipdate.check('matplotlib', '0.4.5')
    print(msg)

will print

::

    Upgrade to   matplotlib 2.0.0    available! (installed: 0.4.5)

    matplotlib's API changes in this upgrade. Changes to your code may be necessary.

    To upgrade matplotlib with pip, type

       pip install -U matplotlib

    To upgrade _all_ pip-installed packages, use

       pipdate/pipdate3

    To disable these checks, set SecondsBetweenChecks in
    /home/jdoe/.config/pipdate/config.ini

If you guard the check with

.. code:: python

    if pipdate.needs_checking('matplotlib'):
        print(pipdate.check('matplotlib', '0.4.5'), end='')

then it will be performed at most every *k* seconds, where *k* is
specified in the config file ``$HOME/.config/pipdate/config.ini``, e.g.,
once a day

::

    [DEFAULT]
    secondsbetweenchecks = 86400

This can, for example, be used by module authors to notify users of
upgrades of their own modules.

Installation
~~~~~~~~~~~~

pipdate is `available from the Python Package
Index <https://pypi.python.org/pypi/pipdate/>`__, so simply type

::

    pip install pipdate

Testing
~~~~~~~

To run the pipdate unit tests, check out this repository and type

::

    pytest

Distribution
~~~~~~~~~~~~

To create a new release

1. bump the ``__version__`` number,

2. publish to PyPi and GitHub:

   ::

       $ make publish

License
~~~~~~~

pipdate is published under the `MIT
license <https://en.wikipedia.org/wiki/MIT_License>`__.

.. |CircleCI| image:: https://img.shields.io/circleci/project/github/nschloe/pipdate/master.svg
   :target: https://circleci.com/gh/nschloe/pipdate/tree/master
.. |codecov| image:: https://img.shields.io/codecov/c/github/nschloe/pipdate.svg
   :target: https://codecov.io/gh/nschloe/pipdate
.. |Codacy grade| image:: https://img.shields.io/codacy/grade/e2b04ea7e4a74da2a80799056b72b189.svg
   :target: https://app.codacy.com/app/nschloe/pipdate/dashboard
.. |PyPi Version| image:: https://img.shields.io/pypi/v/pipdate.svg
   :target: https://pypi.python.org/pypi/pipdate
.. |GitHub stars| image:: https://img.shields.io/github/stars/nschloe/pipdate.svg?style=social&label=Stars
   :target: https://github.com/nschloe/pipdate


