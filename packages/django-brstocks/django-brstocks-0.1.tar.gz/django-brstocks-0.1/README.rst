=====
django-brstocks
=====

django-brstocks is a simple Django app to conduct Web-based Stock Logging.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_brstocks',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('django_brstocks/', include('polls.urls')),

3. Run `python manage.py migrate` to create the brstock models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create new objects(you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/stocks/ begin
