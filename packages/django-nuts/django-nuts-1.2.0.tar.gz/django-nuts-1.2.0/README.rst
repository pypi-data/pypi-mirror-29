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
    load_nuts(), load_ohter_nuts(), load_lau()

    # load NUTS and LAU for some particular countries
    load_nuts('CZ', 'SK'), load_other_nuts('IS'), load_lau('CZ', 'SK')

    # load NUTS and LAU using celery task (requires celery)
    from django_nuts.tasks import load_nuts, load_lau
    load_nuts.delay('CZ'), load_lau.delay('CZ')
