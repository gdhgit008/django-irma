====
IRMA
====

.. image:: https://img.shields.io/pypi/v/django-irma.svg?branch=main
    :target: https://pypi.python.org/pypi/django-irma

IRMA (I Reveal My Attributes) is an attribute-based identity management system. This package provides
IRMA user authentication, authorisation and attribute disclosure for Django. Please visit https://irma.app 
for more information about IRMA. Below you will find a quick start and detailed documentation about the different IRMA functionalities.

-----------
Quick start
-----------

#. Install using pip the django-irma package:

    .. code-block:: bash
        
        pip install django-irma

#. Add "irma.apps.IrmaConfig" to your INSTALLED_APPS setting:

    .. code-block:: python3

        INSTALLED_APPS = [
            ...
            'irma.apps.IrmaConfig',
        ]

#. Add "django_user_agents.middleware.UserAgentMiddleware" to your MIDDLEWARE in settings.py:

    .. code-block:: python3

        MIDDLEWARE = [
            ...
            'django_user_agents.middleware.UserAgentMiddleware', 
        ]

#. Add "irma.irma_auth_backend.IrmaAuthenticationBackend" to your AUTHENTICATION_BACKENDS in setting.py:

    .. code-block:: python3

        AUTHENTICATION_BACKENDS = [
            ...
            'irma.irma_auth_backend.IrmaAuthenticationBackend',
        ]

#. Add the following three IRMA variables to settings.py:

    .. code-block:: python3

        IRMA_SERVER_URL = 'https://www.exampleirmaserverurl.com'
        IRMA_SERVER_PORT = '8088'
        IRMA_SRVER_AUTHENTICATION_TOKEN = os.environ.get('IRMA_SERVER_TOKEN')

   Note: fill in your own IRMA server URL and port. It is recommended to store 
   the IRMA server token in your environment.

#. Include the irma URLconf in your project urls.py:

    .. code-block:: python3

        path('irma/', include('irma.urls')),

#. Add the following line to your base.html to allow the IRMA modal in your project:

    .. code-block:: django

        {% include "irma/modal.html" %}

#. Run the following command to test if the package is installed correctly:

    .. code-block:: bash

        python3 manage.py test irma

The django-irma package offers three functionalities (IRMA user authentication, IRMA authorisation 
and attribute disclosure), which can be implemented independently. The following sections describe 
how to implement each functionality. If you are interested in one specific functionality, you can 
go directly to the respective section without reading the other functionalities. In all 
cases, you need to set up an IRMA server. See the IRMA documentation on how to set up an IRMA 
server. The recommended IRMA server configuration for this Django package can be found at the end
of this page.

------------------------
IRMA user authentication
------------------------
Note: before implementing IRMA user authentication, you must have a Django 
authentication system in place. For more information, see https://docs.djangoproject.com/en/4.0/topics/auth/.
The IRMA user authentication setup consists of registering IRMA users and authenticating IRMA 
users. IRMA user authentication uses the Django User objects with the set_unusable_password() 
method. The authentication attribute value corresponds with the username of the User object.

IRMA register
.............

Add an IRMA register button to your project. Set data-toggle to 'modal' and data-target to '#IRMAmodal'.
Set onclick to the start_irma_session() function. This function takes three string arguments:

#. The IRMA session type, in this case 'IRMA_register'.
#. The URL path of the view you want to redirect to after successful registration.
#. The attribute's identifier you want to use for registration/authentication.

For a list of attribute identifiers, go to https://privacybydesign.foundation/attribute-index/en/. 
Below you find a code example of a button:

.. code-block:: html

    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#IRMAmodal" 
    onclick="start_irma_session('IRMA_register','registration_done', 'pbdf.sidn-pbdf.irma.pseudonym')">
        Register with IRMA
    </button>

You can provide a second and third attribute identifier. The identifiers should be separated with an ampersand symbol. 
When you provide more than one attribute identifier, the first attribute will be used as the username for the IRMA user. 
The second attribute will be stored as the first name and the third attribute will be stored as the last name in the Django user database. 
For example::

    irma−demo.sidn−pbdf.email.email&pbdf.gemeente.personalData.initials&pbdf.gemeente.personalData.surname

**Important note**: your first attribute must be unique for every IRMA user. Examples of unique attributes are email 
address (pbdf.pbdf.email.email) or the pseudonym attribute (pbdf.sidn-pbdf.irma.pseudonym). We suggest you use one of 
those two attributes as a username for your project when new to IRMA. The advantage of using the pseudonym
attribute is that every IRMA user has the attribute installed upon installating the IRMA app. Also, the pseudonym 
attribute is highly privacy friendly. More experienced IRMA users could choose different attributes as a username.

Typically you can redirect to any view you like. The view you redirect to contains in the request.session dictionary a key 'activity_result' 
that can be equal to 'SUCCESS' or 'FAILURE'. This attribute tells you if the IRMA register session was successful or not and can help you 
to determine what you want to show to the user. Suppose you provided a second and third argument, the request.session dictionary keys 'firstname' 
and 'lastname' are also present with IRMA attribute values. Below you find an example of a view after an IRMA registration session:

.. code-block:: python3

    def registration_done(request):
        result = json.loads(request.session['session_result']) 
        parameter1 = request.session['username']
        parameter2 = request.session['firstname']+' '+request.session['lastname']
        if result ['activity_result'] == 'SUCCESS':
            return render(request, 'blog/registration_success.html', {'parameter1' : parameter1 , 'parameter2' : parameter2})
        return render(request, 'blog/registration_failure.html', {'parameter1' : parameter1 , 'parameter2' : parameter2})

IRMA login
..........

Add an IRMA login button to your project. Set data-toggle to 'modal' and data-target to '#IRMAmodal'.
Set onclick to start_irma_session() function. This function takes three string arguments:

#. The IRMA session type, in this case 'IRMA_authenticate'.
#. The URL path of the view you want to redirect to after successful IRMA authentication.
#. The attribute's identifier used during the IRMA registration process.

Below you find a code example of a button:

.. code-block:: html

    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#IRMAmodal" 
    onclick="start_irma_session('IRMA_authenticate','authentication_done', 'pbdf.sidn-pbdf.irma.pseudonym')">
        IRMA Login
    </button>

A second and third attribute can be requested in the same format as in the registration 
section. The view you redirect to has stored the result of the session in 
request.session['session_result']. The session result contains a dictionary with the 
'activity_result' to indicate if the authentication was successful ('SUCCESS') or 
not ('FAILURE'). Below you find an example of a view which is redirected to after 
an IRMA authentication session:

.. code-block:: python3

    def authentication_done(request):
        result = json.loads(request.session['session_result']) 
        if result['activity_result'] == 'SUCCESS':
            parameter1 = request.user.username
            parameter2 = request.user.first_name+' '+request.user.last_name
            return render(request, 'blog/authentication_success.html', {'parameter1' : parameter1 ,'parameter2' : parameter2})
        return render(request, 'blog/authentication_failure.html', {})

If the IRMA authentication session was successful, the IRMA user is now associated 
with its corresponding User object in the Django user database.

------------------
IRMA authorisation
------------------
IRMA can provide access control to views by verifying the attributes of an IRMA
user. If the IRMA user owns the requested attribute value(s), the
user can access the view. If the user cannot disclose the requested attribute
value(s), the user will be shown a message and is not forwarded to the requested
view. IRMA stores authorisation details in a Django session. If the session
is destroyed, the IRMA authorisation details are also destroyed. This package
removes a session at browser closure. However, some browsers automatically
rebuilt a session when being reopened. In such case, the IRMA authorisation 
details are not removed during browser closure. Because this package relies 
heavily on Django sessions, you should set the SESSION_COOKIE_SECURE in 
setting.py to True if you have an SSL-enabled site.

Add a button to your project. Set data-toggle to 'modal' and data-target to '#IRMAmodal'.
Set onclick to start_irma_session() function. This function takes four string arguments:

#. The IRMA session type, in this case 'IRMA_authorise'.
#. The URL path of the view you want to redirect to after a successful IRMA authorisation session.
#. The identifier of the required attribute(s).
#. The attribute value(s) for successful IRMA authorisation.

If more than one attribute is requested, attribute identifiers must be concatenated 
with an ampersand (&). When multiple attributes are requested, multiple attribute 
values must be given in the same order as the attributes are requested.
Below you find a code example:

.. code-block:: html

    <button type="button" class=" btn btn−primary" data−toggle="modal" data−target="#IRMAmodal" 
    onclick="start_irma_session('IRMA_authorise', 'universitystudent',
    'irma−demo.RU.studentCard.university&irma−demo.RU.studentCard.level', 'Open Universiteit&Bachelor')">
        Authorise with IRMA
    </button>

In this example, students will pass the IRMA authorisation when their irma−demo.RU.studentCard.university
attribute value equals 'Open University' and their attribute irma−demo.RU.studentCard.level equals
'Bachelor'. The syntax of the fourth argument must precisely match the requested attribute value.
After adding the button for IRMA users to prove specific properties, IRMA authorisation 
works with the @irma_authorisation_required decorator. The decorator takes three arguments:

#. A string of attributes (separated with an ampersand if multiple attributes are required) must be verified before access is given to the view.
#. A string that is shown as a message to the user if the user tries to access a view for which it has no IRMA access permission.
#. A string that is shown if the user passes the IRMA authorisation session.

Below you find an example:

.. code-block:: python3

    @irma_authorisation_required('irma-demo.RU.studentCard.university',settings.UNIVERSITY_CHECK_REQUIRED,settings.UNIVERSITY_CHECK_PASSED)

The decorator should be placed above a function-based view in views.py for
which you want to use IRMA authorisation. In this example, only students
with a university attribute value specified in the button's
onclick can access the view. The string messages can be passed as a settings.py variable 
(as in this example) or can be passed as a string argument to the decorator.
You can specify the following strings for IRMA authorisation messages in settings.py::

    AUTHORISATION_FAILURE: string for the message when a user did not pass the IRMA authorisation session.
    AUTHORISATION_PARTIAL: string for the message when a user only possesses a subgroup of the required authorisation attributes.
    AUTHORISATION_REMOVED: string for the message when previous authorisations are cancelled.

*Known limitations*: IRMA authorisation is only available for function-based views. No 
mixin is available yet for class-based views.
IRMA Authorisation cannot handle attributes used for multiple views but require
different attribute values for different views. For example, you cannot make a view for 
only Open Universiteit students (irma−demo.RU.studentCard.university attribute value 
should equal 'Open Universiteit') and a view for 'UVA' students only 
(irma−demo.RU.studentCard.university attribute value should equal 'UVA'). The 
authorisation allows only to verify one attribute value for all views.

-------------------------
IRMA attribute disclosure
-------------------------
It is possible to request attribute values from IRMA users. For example, if you want 
to send a package to an IRMA user, you can request the IRMA user's address or phone number.
Add a button to your project. Set data-toggle to 'modal' and data-target to '#IRMAmodal'.
Set onclick to start_irma_session() function. This function takes three arguments:

#. The IRMA session type, in this case 'IRMA_disclose'.
#. The URL path of the view you want to redirect to after a successful IRMA disclosure session.
#. The attribute's identifier that you want to receive.

Below you find an example of a button that requests for an IRMA user's mobile number:

.. code-block:: html

    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#IRMAmodal" 
    onclick="start_irma_session('IRMA_disclose','disclosure_start', 'pbdf.sidn-pbdf.mobilenumber.mobilenumber')">
        Complete form with IRMA
    </button>

The view to which IRMA redirects the user after a disclosure session stores the requested 
attributes with the attribute values in request.session['disclose_attributes']. The 
dictionary key 'disclose_attributes' contains a dictionary as a value. The dictionary as a
value contains all requested attributes identifiers as a key and attributes values as 
a value of the dictionary. Below we give you an example of how a view could handle 
the disclosed attributes:

.. code-block:: python3

    def disclosure_start(request):
        street = ''
        mobilenumber = ''
        if 'disclosed_attributes' in request.session:
            if 'pbdf.gemeente.address.street' in request.session['disclosed_attributes']:
                street = request.session['disclosed_attributes']['pbdf.gemeente.address.street']

            if 'pbdf.sidn-pbdf.mobilenumber.mobilenumber' in request.session['disclosed_attributes']:
                mobilenumber = request.session['disclosed_attributes']['pbdf.sidn-pbdf.mobilenumber.mobilenumber']

        return render(request, 'blog/disclosure_start.html',{'street': street, 'mobilenumber': mobilenumber})


-------------------------
IRMA server configuration
-------------------------
This Django package is only tested on one specific IRMA server configuration. With 
different IRMA server configurations, you might experience unexpected behaviour in 
Django. The IRMA server configuration used for this Django package: 

.. code-block:: json

    {
        "schemes_path": "/etc/irmaserver",
        "schemes_assets_path": "",
        "disable_schemes_update": false,
        "schemes_update": 60,
        "privkeys": "",
        "url": "https://www.example.com:8088",
        "disable_tls": false,
        "email": "example@email.com",
        "enable_sse": false,
        "store_type": "",
        "redis_settings": null,
        "static_sessions": null,
        "max_session_lifetime": 5,
        "jwt_issuer": "irmaserver",
        "jwt_privkey": "",
        "jwt_privkey_file": "",
        "allow_unsigned_callbacks": false,
        "augment_client_return_url": false,
        "verbose": 1,
        "quiet": false,
        "log_json": false,
        "revocation_db_str": "",
        "revocation_db_type": "",
        "revocation_settings": {},
        "production": true,
        "disclose_perms": ["*"],
        "sign_perms": ["*"],
        "issue_perms": ["*"],
        "revoke_perms": [],
        "skip_private_keys_check": false,
        "no_auth": false,
        "listen_addr": "",
        "port": 8088,
        "api_prefix": "/",
        "tls_cert": "",
        "tls_cert_file": "/etc/letsencrypt/live/www.example.com/fullchain.pem",
        "tls_privkey": "",
        "tls_privkey_file": "/etc/letsencrypt/live/www.example.com/privkey.pem",
        "client_port": 0,
        "client_listen_addr": "",
        "client_tls_cert": "",
        "client_tls_cert_file": "",
        "client_tls_privkey": "",
        "client_tls_privkey_file": "",
        "requestors": {"<djangowebsite>": {"auth_method": "token","key": "<irma_server_token>"}},
        "max_request_age": 300,
        "static_path": "",
        "static_prefix": "/"
    }

---------------
Undo activities
---------------

All activities (IRMA register, authenticate, authorise and disclose) can be undone. 
This can be handy when testing a website. For example, you want to log in and 
log out multiple times without closing the browser to delete the session.
To de-register an IRMA user from the Django user database, add the following 
button (should only be visible for authenticated IRMA users):

.. code-block:: html

    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#IRMAmodal" 
     onclick="start_irma_session('IRMA_unregister','unregistration_done')">
        Remove my user profile
    </button>

To log out an IRMA user add the following button (should only be visible for authenticated IRMA users):

.. code-block:: html

    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#IRMAmodal" 
     onclick="start_irma_session('IRMA_unauthenticate','unauthentication_done')">
        Log out with IRMA
    </button>

To clear all IRMA authorisation add the following button:

.. code-block:: html

    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#IRMAmodal" 
     onclick="start_irma_session('IRMA_clear_authorisations','display_authorisations')">
        Clear authorisation with IRMA
    </button>

To clear all disclosed attribute value add the following button:

.. code-block:: html

    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#IRMAmodal" 
     onclick="start_irma_session('IRMA_clear_disclose','display_disclosed')">
        Clear personal data with IRMA
    </button>

---------
More info
---------
A demo website is available on https://www.irmadjangoapi.nl.
The source code of this project can be found on GitHub: https://github.com/gdhgit008/django-irma.
More technical information about IRMA: https://irma.app/ docs/what-is-irma/.
More information about Django: //docs.djangoproject.com/en/4.0/.
