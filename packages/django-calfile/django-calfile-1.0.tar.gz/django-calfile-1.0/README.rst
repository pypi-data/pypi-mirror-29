=====
Calendar File
=====

CalFile is a simple Django app to create a calendar file.

Detailed documentation is in the "docs" directory.

Quick start
----------------------
1. Install
    pip install django-calfile
    
2. Add "calfile" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'calfile',
    ]

3. define::
    CALFILE_DATE_FORMAT = '%d-%m-%Y %H:%M'

4. Include the URLconf in your project urls.py like this::

    path('calfile/', include('calfile.urls')),

5. Post /calfile/ with parameters (start_date, end_date).