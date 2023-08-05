=============================
Django RQ Pulse
=============================

.. image:: https://badge.fury.io/py/django-rq-pulse.svg
    :target: https://badge.fury.io/py/django-rq-pulse

.. image:: https://travis-ci.org/NZME/django-rq-pulse.svg?branch=master
    :target: https://travis-ci.org/NZME/django-rq-pulse

A Django package to check that rq workers are running and notify admins if they are not

Quickstart
----------

Install Django RQ Pulse::

    pip install django-rq-pulse

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_rq_pulse.apps.DjangoRqPulseConfig',
        ...
    )

Define the `DEFAULT_FROM_EMAIL` and `ADMINS` Django settings because these settings will be used to send notification emails.

Define a dictionary in your Django settings for your Redis connection details like so::

    REDIS_DB = {
        'host': 'Your Redis Hostname or IP goes here',
        'port': 'Your Redis port number goes here',
        'database': 'Your Redis database number goes here'
    }

Usage
--------

Check that rqworkers are running::

    $ python manage.py rq_pulse_check

If the actual number of workers is not equal the expected number of workers or
If there are items in the queue but the queue size is not changing notify admins by email.

The above command will run with default parameters where::

    --expected-num-workers=2
    --seconds-to-sleep=5
    --num-retries=5
    --queue-name="default"

You can override these values by passing any or all the parameters to the command like so::

    $ python manage.py rq_pulse_check --expected-num-workers=3 --queue-name="high"

To get a list of the command parameters use the --help parameter::

    $ python manage.py rq_pulse_check --help

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.3 (2018-02-12)
++++++++++++++++++

* Add commands to Makefile to simplify the package build and release process

0.1.2 (2018-02-12)
++++++++++++++++++

* Modify setup.py to enable the usage of bumpversion.

0.1.1 (2018-02-12)
++++++++++++++++++

* Allow the Redis connection details to be customizable.

0.1.0 (2018-01-19)
++++++++++++++++++

* First release on PyPI.


