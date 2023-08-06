Tox-Pipenv
==========

.. image:: https://img.shields.io/pypi/v/tox-pipenv.svg
        :target: https://pypi.python.org/pypi/tox-pipenv

.. image:: https://img.shields.io/travis/tonybaloney/tox-pipenv.svg
        :target: https://travis-ci.org/tonybaloney/tox-pipenv

.. image:: https://codecov.io/gh/tonybaloney/tox-pipenv/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/tonybaloney/tox-pipenv

.. image:: https://pyup.io/repos/github/tonybaloney/tox-pipenv/shield.svg
     :target: https://pyup.io/repos/github/tonybaloney/tox-pipenv/
     :alt: Updates

.. image:: https://pyup.io/repos/github/tonybaloney/tox-pipenv/python-3-shield.svg
     :target: https://pyup.io/repos/github/tonybaloney/tox-pipenv/
     :alt: Python 3

A Tox plugin to replace the default use of virtualenv with Pipenv.

This is a convenient way to retain your use of Pipenv, whilst testing multiple versions of Python.

Installation
------------

.. code-block:: bash

    pip install tox-pipenv

Or, 

.. code-block:: bash

    pipenv install tox-pipenv  

Creating virtual environments
-----------------------------

With this plugin, tox will use `pipenv --python {python binary}` as given to the tox interpreter for each python path.

If you already have virtual environments cached with tox, use the --recreate flag to recreate them with pipenv.

Note: Tox will pass the --site-packages flag to pipenv if this is configured in your Tox config.

The Pipfile will exist in .tox/{env}/Pipfile as well as Pipfile.lock

Installing requirements
-----------------------

The installation of requirements from your tox config will be passed to pipenv install for installation into the virtual 
environment. This replaces the use of pip within tox.

``requirements.txt`` files will also be parsed by Pipenv and used for each test environment

Executing tests
---------------

Each of the commands in your testenv configuration will be passed to pipenv to execute within the pipenv virtual environment


TODO
----

This plugin needs work, namely: 

* Tox always calls `pip freeze` to show versions, this is not yet pluggable

Authors
-------

* Anthony Shaw
* Omer Katz

Release notes
=============

1.4.0 (2018-03-08)
------------------

* Bugfix : Fixed error "LocalPath object has no attribute endswith"
* Bugfix : Fixed error "Cannot run tox for the first time with this plugin installed"

1.3.0 (2018-03-03)
------------------

* Bugfix : fixed issue when Pathlib.Path occured instead of string
* Update : updated pipenv to 11.0.1

1.2.1 (2018-01-08)
------------------

* Added documentation and fixed pypi build

1.2.0 (2018-01-08)
------------------

* Virtual environments are now correctly stored in .tox/<pyver>/.venv
* Packages will be reported by pipenv graph after installation. Pip freeze is still being run, downstream PR raised in tox
* Plugin should not accidentally remove host virtualenv binaries

1.1.0 (2017-12-30)
------------------

* Use Pipenv install --dev as the default installation command

1.0.0 (2017-12-22)
------------------

* Support for creation and recreation of virtual environments using Pipenv
* Isolation of Pipfile within the tox directory
* Support for installation of tox-specified packages in Pipenv
* Support for execution of test commands within a Pipenv virtual env


