django-ohm2-handlers-light source code
=============================


Installation:

#. Create a Python +3.5 virtualenv

#. Install dependencies::

    - ohm2_handlers_light

#. Add 'ohm2_countries_light' to installed apps::

    INSTALLED_APPS = [
      '''
      'ohm2_countries_light',
      ...
    ]

#. Create tables::

    ./manage.py migrate




Models
------

ohm2_countries_light comes with one basic Country models:


Variables
---------

OHM2_COUNTRIES_LIGHT_FLAGS_SMALL_BASE_PATH: path to small flag images (the pages comes with default ones)


API - v1
--------




	