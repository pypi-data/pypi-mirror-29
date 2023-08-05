============
Task Tracker
============
Task Tracker is a basic Django app to record and track stories, tasks
and invested time. Loosely based on Extreme Programming methodology.

Quick start
-----------

1. Use an old Django project or start a new project in desired location::
	
	$ django-admin startproject mysite

2. In your project settings.py add "tracker" to INSTALLED_APPS like this::

    INSTALLED_APPS = [
        ...
        'tracker',
    ]

3. Include the tracker URLconf in your project urls.py like this::

    path('tracker/', include('tracker.urls')),

4. Create Task Tracker models by runing::

	$ python manage.py migrate

5. Start the development server::

	$ python manage.py runserver

6. Visit http://127.0.0.1:8000/tracker/.

Tests
-----

App has inbuilt tests that require Selenium set up. See
http://www.seleniumhq.org for more details.