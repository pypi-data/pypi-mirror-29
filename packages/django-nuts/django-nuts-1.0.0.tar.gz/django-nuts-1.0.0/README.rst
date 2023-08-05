Django NUTS
===========

Django application providing database of European NUTS and LAU

Installation
------------

.. code:: shell

    pip install django-nuts


Configuration
-------------

Add ``'django_nuts'`` to ``settings.INSTALLED_APPS``.


Data migration
--------------

.. code:: shell

    python manage.py migrate


Load / update data
------------------

You may load the data manually from the shell (``python manage.py shell``)

.. code:: python

    from django_nuts import load_nuts, load_lau

    # load all NUTS and LAU (note that nuts must be loaded first)
    load_nuts(), load_lau()

    # load NUTS and LAU for some particular country
    load_nuts('CZ'), load_lau('CZ')

    # load NUTS and LAU using celery task (requires celery)
    from django_nuts.tasks import load_nuts, load_lau
    load_nuts.delay('CZ'), load_lau.delay('CZ')
