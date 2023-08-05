=====================
Django Health Checker
=====================

Django health checker is a simple Django app to conduct health checking which
uses django-health-check (https://github.com/KristianOellegaard/django-health-check)
and overrides default behavior.


Quick start
-----------

1. Include the health_checker URLconf in your project urls.py like this::

    path('health-checker/', include('health_checker.urls')),

2. Start the development server and visit http://127.0.0.1:8000/health-checker/
   to get a 'pong' response if every health check has passed.


