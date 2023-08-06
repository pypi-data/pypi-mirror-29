=====
Adhara
=====

Adhara in sanskrit meaning base/foundation, is a foundation for using Django as a Rest API provider.
Not just as a rest API provider, but much more.
Adhara handles sessions over Django sessions, events to fire to Android, Web, IOS, etc.
Also Adhara provides abstract models that can be extended to implementing apps to provide full REST API support.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "adhara" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'adhara',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^adhara/', include('adhara.urls')),

3. Run the following command to create the adhara Event models.::

    python manage.py migrate

