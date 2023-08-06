===============================
djangocms-maps |latest-version|
===============================

|build-status| |health| |python-support| |license| |gitter|

A universal maps plugin for django CMS, supporting all major map providers.

Supported online map providers:

- Mapbox OpenStreetMap *powered by* `Leaflet.js`_
- Bing Maps
- Google Maps
- HERE WeGo
- ViaMichelin

All map providers require an API key, which you usually get for free by
creating a developer account (using the links below).

Installation
============

This plugin requires `django CMS`_ 3.3 (and Django 1.8) or above.

* In your project's `virtualenv`_, run ``pip install djangocms-maps``.
* Add ``'djangocms_maps'`` to your ``INSTALLED_APPS`` setting.
* Run ``manage.py migrate djangocms_maps``.

Configuration
=============

``MAPS_PROVIDERS = [ ('<str>', '<str>'), ... ]``
------------------------------------------------
Optional.  Allows you to specify the providers you want to offer, their
display labels and sort order in the user interface.  Put a provider on top
of the list to make it the default.  **Default:**

.. code-block:: python

    MAPS_PROVIDERS = [
        ('mapbox', _('Mapbox OSM (API key required)')),
        ('bingmaps', _('Bing Maps (API key required)')),
        ('googlemaps', _('Google Maps (API key required)')),
        ('here', _('HERE WeGo (API key required)')),
        ('viamichelin', _('ViaMichelin (API key required)')),
    ]

``MAPS_BINGMAPS_API_KEY = '<str>'``
-----------------------------------
`API key for Bing Maps`_ (required for using Bing Maps).

``MAPS_GOOGLEMAPS_API_KEY = '<str>'``
-------------------------------------
`API key for Google Maps`_ (required for using Google Maps).

``MAPS_HERE_API_KEY = {'app_id': '<str>', 'app_code': '<str>'}``
----------------------------------------------------------------
`APP_ID and APP_CODE for HERE WeGo`_ (required for using HERE maps).

``MAPS_MAPBOX_API_KEY = '<str>'``
---------------------------------
`Access token for Mapbox`_ (required for using OSM maps with Mapbox tile layers).

``MAPS_VIAMICHELIN_API_KEY = '<str>'``
--------------------------------------
`API key for ViaMichelin`_ (required for using ViaMichelin maps).

Examples
========

:Organice Demo:
    https://demo.organice.io/about/directions/

    Your maps plugin playground! Allows you to directly edit and view (albeit
    not to publish) changes on the maps plugin after authenticating.

Translations
============

If you want to help translate the plugin please do it on `transifex`_.

Developer Resources
===================

- Bing:
  - `Dev Center <https://www.bingmapsportal.com/>`__
  - `docs overview <https://msdn.microsoft.com/en-us/library/dd877180.aspx>`__
  - `API docs <https://msdn.microsoft.com/en-us/library/mt712552.aspx>`__
  - `examples <http://www.bing.com/api/maps/sdk/mapcontrol/isdk>`__
- Google:
  - `API docs <https://developers.google.com/maps/documentation/javascript/>`__
- HERE:
  - `API docs <https://developer.here.com/javascript-apis/documentation/v3/maps/topics/api-reference.html>`__
  - `examples <https://developer.here.com/api-explorer/maps-js/>`__
- Mapbox.js / Leaflet.js:
  - `API docs <https://www.mapbox.com/mapbox.js/api/>`__
  - `examples <https://www.mapbox.com/mapbox.js/examples/>`__
  - `Leaflet API docs <http://leafletjs.com/reference.html>`__
- ViaMichelin:
  - `API docs <http://dev.viamichelin.com/map-service.html>`__


.. |latest-version| image:: https://img.shields.io/pypi/v/djangocms-maps.svg
   :alt: Latest version on PyPI
   :target: https://pypi.python.org/pypi/djangocms-maps
.. |build-status| image:: https://img.shields.io/travis/Organice/djangocms-maps/master.svg
   :alt: Build status
   :target: https://travis-ci.org/Organice/djangocms-maps
.. |health| image:: https://landscape.io/github/Organice/djangocms-maps/master/landscape.svg?style=flat
   :target: https://landscape.io/github/Organice/djangocms-maps/master
   :alt: Code health
.. |python-support| image:: https://img.shields.io/pypi/pyversions/djangocms-maps.svg
   :target: https://pypi.python.org/pypi/djangocms-maps
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/djangocms-maps.svg
   :alt: Software license
   :target: https://github.com/Organice/djangocms-maps/blob/master/LICENSE.txt
.. |gitter| image:: https://badges.gitter.im/Organice/djangocms-maps.svg
   :alt: Gitter chat room
   :target: https://gitter.im/Organice/chat

.. _Leaflet.js: http://leafletjs.com/
.. _django CMS: https://github.com/divio/django-cms
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _API key for Bing Maps: https://msdn.microsoft.com/en-us/library/mt712556.aspx
.. _API key for Google Maps:
    https://developers.google.com/maps/documentation/javascript/get-api-key
.. _APP_ID and APP_CODE for HERE WeGo:
    https://developer.here.com/javascript-apis/documentation/v3/maps/common/credentials.html
.. _Access token for Mapbox: https://www.mapbox.com/help/create-api-access-token/
.. _API key for ViaMichelin:
    http://business-solutions.travel.michelin.com/contact-us/open-a-free-api-test-account.html
.. _transifex: https://www.transifex.com/divio/djangocms-maps/
