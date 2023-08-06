molo.surveys
=============================

.. image:: https://img.shields.io/travis/praekelt/molo.pwa.svg
        :target: https://travis-ci.org/praekelt/molo.pwa

.. image:: https://img.shields.io/pypi/v/molo.pwa.svg
        :target: https://pypi.python.org/pypi/molo.pwa

.. image:: https://coveralls.io/repos/praekelt/molo.pwa/badge.png?branch=develop
    :target: https://coveralls.io/r/praekelt/molo.pwa?branch=develop
    :alt: Code Coverage

An implementation of pwa as a Molo plugin

Installation::

  pip install molo.pwa


Django setup::

  INSTALLED_APPS = [
      ...
      'molo.pwa',
      'fcm_django',
      ...
  ]

Configure serviceworker path, app name, description, icons, and FCM::

  PWA_SERVICE_WORKER_PATH = join(
      PROJECT_ROOT, 'your_app', 'templates', SITE_LAYOUT_BASE, 'serviceworker.js')
  PWA_NAME = 'App Name'
  PWA_DESCRIPTION = 'App Description'
  PWA_THEME_COLOR = '#fff'
  PWA_DISPLAY = 'standalone'
  PWA_START_URL = '/'
  PWA_ICONS = [
      {
          'src': '/static/img/appicons/app_icon.png',
          'sizes': '160x160',
          "type": "image/png"
      }
  ]
  PWA_FCM_API_KEY = 'FCM API KEY'
  PWA_FCM_MSGSENDER_ID = 'FCM MESSAGE SENDER ID'
  FCM_DJANGO_SETTINGS = {
          "FCM_SERVER_KEY": 'FCM SERVER KEY',
          "ONE_DEVICE_PER_USER": True,
          "DELETE_INACTIVE_DEVICES": False,
  }


In your urls.py::

  urlpatterns = [
      url(r'', include('molo.pwa.urls')), 
      ...
      ...
  ]

In your base.html::

  {% load molo_pwa %}

  <head>
      ...
      {% molo_pwa_meta %}
      ...
  </head>

