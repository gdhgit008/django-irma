=====
IRMA
=====

IRMA I Reveal My Attributes is a Django app to for IRMA functionality. The app provides
IRMA user authentication, authorisation and attribute disclosure.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "irma.apps.IrmaConfig" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'irma.apps.IrmaConfig',
    ]

2. Add "irma.irma_auth_backend.IrmaAuthenticationBackend" to your AUTHENTICATION_BACKENDS setting like this::
    
    AUTHENTICATION_BACKENDS = [
        ...
        'irma.irma_auth_backend.IrmaAuthenticationBackend',
    ]

2. Include the irma URLconf in your project urls.py like this::

    path('irma/', include('irma.urls')),

3. Run ``python manage.py migrate`` to create the irma models.

4. Visit "docs" directory for how to use the IRMA app.