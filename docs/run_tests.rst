Running ``django-dfk`` test suite
=================================

``django-dfk`` has been configured to work with the ``tox`` package to ensure cross python / django compatibility.
The ``tox.ini`` file in the root of the source defines which versions of Python ``django-dfk`` should be tested against along
with all the applicable versions of django that we aim to support.

Running tests with tox
======================

To run the test suite with tox ``django-dfk`` needs to be installed as an editable egg eg.::

    pip install -e git+ssh://git@github.com/danfairs/django-dfk.git#egg=django-dfk

or be a clone of the checkout with the ``PYTHONPATH`` and ``DJANGO_SETTINGS_MODULE`` environment variables handled accordingly.

Next you need to install tox into your virtualenv::

    pip install tox

Finally you need to make sure you have system installs of all the versions of Python we wish to test against (currently Python 2.6, 2.7, 3.2 and 3.3)

Installing Python versions
==========================

If you are working on Ubuntu, you can use the Deadsnake PPA repositories to install all of these versions of Python.
Here is the steps that I took on Ubuntu Desktop 12.04 to get all the python versions setup::

    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python3.3
    sudo apt-get install python3.2
    sudo apt-get install python2.6

Please note that the above commands install the ``minimal`` install of each version of Python. Python 3.3 and Python 2.6 also have ``complete`` versions e.g ``sudo apt-get install python2.6-complete``. These versions also install the ``dev`` headers, ``dbg`` libraries etc. It's up to you what you want to install. I tend to air on the side of caution and installed the ``complete`` versions for the sake of being thorough. There is no ``complete`` version for Python 3.2 in Deadsnakes PPA repositories, so if you need the extra libs then you will need to install them manually.

Once all your versions of Python are installed and available, you can run the test suite with tox.

1. Activate the virtualenv that you installed ``django-dfk`` and ``tox`` into.
2. Run the test suite with tox using the below command

::

    tox

The first build through will be quite slow whilst it builds each ``virtualenv`` agaisnt each version of Python along with the specified version of django and runs the tests. Subsequent runs should be much quicker as ``tox`` leaves the ``virtualenv`` in place by default in a folder named ``.tox``

Run tests quickly
=================

You don't have to use ``tox`` to run the test suite. If you are making changes to ``django-dfk`` and just want a quick run through on the current version of Python and install Django, then you can run tests as normal using django's inbuilt management command::

    django-admin.py test dfk --settings=dfk.test_settings
