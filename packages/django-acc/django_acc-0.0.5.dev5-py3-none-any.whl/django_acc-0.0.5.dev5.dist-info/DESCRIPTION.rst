DON'T USE ME. I'M BEING USED INTERNALLY ONLY.

Django-acc: Another reusable DjangoRestFramework account management
application

Installation
============

``pip install django-acc``

Requirements
------------

-  django >= 2.0
-  djangorestframework >= 3.7.7

Configurations
--------------

settings.py
~~~~~~~~~~~

-  Add ``rest_framework``, ``rest_framework.authtoken``, ``django_acc``
   to INSTALLED\_APPS
-  Set

   ::

       REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': (
           'rest_framework.authentication.TokenAuthentication',
       ),
       'DEFAULT_PERMISSON_CLASSES': (
           'rest_framework.permissions.IsAuthenticated'
       )
       }

urls.py
~~~~~~~

-  Add ``path('accounts/', include('accounts.urls'))`` to
   ``urlpatterns`` in your project's ``urls.py``

Features
========

-  api views for creating users ('/accounts/register/') and logging in
   users ('/accounts/login/')
-  Organization management (WIP)

Concepts
========

*Organization* An organization is a group of accounts. It's optional to
create a new organization, but when a new user is created, a default
organization with the same name is also created.


