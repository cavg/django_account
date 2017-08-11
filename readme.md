Basic account functionality
--------------------------

Account is a App for handle relation with a company (belongs to...) and basic auth features:

* Signin
* Signout
* Password recovery
* Password reset


Reusable package
---------------

Packing directory is located in "package"

Instruction for install

`sh install.sh`


Quick start
-----------

1. Add "account" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'account',
    ]

2. Include the polls URLconf in your project urls.py like this::

    from django.conf.urls import include
    url(r'^account/', include('account.urls')),

3. Run `python manage.py migrate` to create the account models (entites company and account).

4. Configurations

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a account (you'll need the Admin app enabled).


Dependencies
------------
Tested for versions:

* Django==1.11.2
* Python==3.6.1