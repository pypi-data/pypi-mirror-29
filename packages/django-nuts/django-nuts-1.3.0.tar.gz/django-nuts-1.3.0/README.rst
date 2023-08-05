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

    from django_nuts.loaders import load_nuts, load_lau, load_other_nuts

    # load all NUTS and LAU (note that NUTS must be loaded before LAU)
    load_nuts(), load_ohter_nuts(), load_lau()

    # load NUTS and LAU for some particular countries
    load_nuts('CZ', 'SK'), load_other_nuts('IS'), load_lau('CZ', 'SK')

    # load NUTS4 for CZ or SK
    from django_nuts.loaders.cz_nuts import load_cz_nuts
    from django_nuts.loaders.sk_nuts import load_sk_nuts
    load_cz_nuts(), load_sk_nuts()

    # load CZ NUTS4 + LAU
    from django_nuts.loaders.cz_nuts4_lau import load_cz_nuts4_lau
    load_cz_nuts4_lau()
