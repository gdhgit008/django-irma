=====
IRMA
=====

IRMA I Reveal My Attributes is a Django app to for IRMA functionality. The app provides
IRMA user authentication, authorisation and attribute disclosure. Please visit https://irma.app 
for more information about IRMA (I Reveal My Attributes). More information about Django can be 
found on https://docs.djangoproject.com/en/4.0/.

Below you find detailed documentation about the different functionalities.

Quick start
-----------

1. Install the django-irma package::
    
    pip install django-irma

2. Add "irma.apps.IrmaConfig" to your INSTALLED_APPS setting::

    INSTALLED_APPS = [
        ...
        'irma.apps.IrmaConfig',
    ]

3. Add "django_user_agents.middleware.UserAgentMiddleware" to your MIDDLEWARE in settings.py::

    MIDDLEWARE = [
        ...
        'django_user_agents.middleware.UserAgentMiddleware', 
    ]

4.  Add "irma.irma_auth_backend.IrmaAuthenticationBackend" to your AUTHENTICATION_BACKENDS in setting.py::

    AUTHENTICATION_BACKENDS = [
        ...
        'irma.irma_auth_backend.IrmaAuthenticationBackend',
    ]

5. Add the following three IRMA variables to settings.py::

    IRMA_SERVER_URL = 'https://www.exampleirmaserverurl.com'
    IRMA_SERVER_PORT = '8088'
    IRMA_SRVER_AUTHENTICATION_TOKEN = os.environ.get('IRMA_SERVER_TOKEN')

    Note: it is recommended to store the IRMA server token in your environment.

6. Include the irma URLconf in your project urls.py::

    path('irma/', include('irma.urls')),

7. Add the following line to your base.html to allow the IRMA modal in your project::

    {% include "irma/modal.html" %}

8. Run the tests to check the pacakge is installed corectly::

    python3 manage.py test irma



The django-irma package offers three functionalities "(IRMA user authentica- tion, IRMA authorisation 
and attribute disclosure)", which can be implemented independently. The next three sections describe 
how to implement each func- tionality. If you are interested in one specific functionality, you can 
go directly to the respective section without the need of reading the other functionalities. In all 
cases, you need to have setup an IRMA server. See the IRMA documenta- tion how to setup an IRMA 
server. In section 3 the recommended IRMA server configuration for this Django package.

IRMA user authentication
------------------------
test tekst


IRMA authorisation
------------------

IRMA attribute disclosure
-------------------------


IRMA server configuration
-------------------------

Undo activities
---------------