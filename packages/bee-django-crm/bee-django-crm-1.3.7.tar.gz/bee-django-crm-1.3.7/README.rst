=====
crm
=====

Quick start
-----------

1. Add "crm" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'crm.apps.CrmConfig',
    )

2. Include the crm URLconf in your project urls.py like this::

    from django.conf.urls import include, url
    ...
    url(r'^crm/', include('crm.urls', namespace='crm')),

3.settings.py like this::

    USER_TABLE="" #用户表，如果用django自带，为空或None。如果自定义，则为app_label.ModelName

3. Run `python manage.py makemigrations`,`python manage.py migrate` to create the crm models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a cc (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/cc/ to participate in the cc.