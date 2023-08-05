=====
Location Maps
=====

Location é um projeto para simplificar todas as implementações de mapas no admin do django

Quick start
-----------

1. Add "location" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'location',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^location/', include('location.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/location/ to participate in the poll.