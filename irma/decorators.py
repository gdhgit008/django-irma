# https://realpython.com/primer-on-python-decorators/
# https://docs.djangoproject.com/en/2.2/_modules/django/contrib/auth/decorators/
from functools import wraps
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.html import format_html

def irma_authorisation_required(attributes, negativeText="", positiveText=""):
    """ 
    Decorator that checks if a visitor is authorised by IRMA before proceeding
    """
    def decorator_wrapper(view_func):
        @wraps(view_func)
        def _wrapper_irma_authorisation_required(request, *args, **kwargs):
            if 'authorisation_removed' in request.session:
                del request.session['authorisation_removed']
                messages.info(request, format_html(settings.AUTHORISATION_REMOVED))
                return redirect(request.META.get('HTTP_REFERER'))
            if 'authorisation_failed' in request.session and request.session['authorisation_failed']:
                del request.session['authorisation_failed']
                messages.info(request, format_html(settings.AUTHORISATION_FAILURE))
                return redirect(request.META.get('HTTP_REFERER'))
            
            user_has_all_required_attributes = True
            user_has_partialy_required_attributes = False
            attribute_list = attributes.split('&')
            for attribute in attribute_list:
                # check if authorised_attributes already exist in session
                if 'authorised_attributes' in request.session:
                    if attribute not in request.session['authorised_attributes']:
                        user_has_all_required_attributes = False
                    else:
                        user_has_partialy_required_attributes = True
                else:
                    user_has_all_required_attributes = False
            if user_has_all_required_attributes:
                if 'displayed_attributes' in request.session:
                    display_positive_text = False
                    for attribute in attribute_list:
                        if attribute not in request.session['displayed_attributes']:
                            display_positive_text = True
                            request.session['displayed_attributes'] = request.session['displayed_attributes']+[attribute]
                else:
                    display_positive_text = True
                    request.session['displayed_attributes'] = [attributes]
                if display_positive_text:
                    messages.success(request, positiveText)
                # Do something before
                view_func(request, *args, **kwargs)
                # Do something after
                return view_func(request, *args, **kwargs)

            elif user_has_partialy_required_attributes:
                messages.info(request, format_html(settings.AUTHORISATION_PARTIAL))
            else:
                messages.info(request, format_html(negativeText))
            return redirect(request.META.get('HTTP_REFERER'))
        return _wrapper_irma_authorisation_required
    return decorator_wrapper

def irma_authorisation_message():
    """ 
    Decorator that checks if a visitor is authorised by IRMA before proceeding
    """
    def decorator_wrapper(view_func):
        @wraps(view_func)
        def _wrapper_irma_authorisation_message(request, *args, **kwargs):
            if 'authorisation_removed' in request.session:
                del request.session['authorisation_removed']
                messages.info(request, format_html(settings.AUTHORISATION_REMOVED))
                return view_func(request, *args, **kwargs)
            if 'authorisation_failed' in request.session:
                if request.session['authorisation_failed']:
                    del request.session['authorisation_failed']
                    messages.info(request, format_html(settings.AUTHORISATION_FAILURE))
                    return view_func(request, *args, **kwargs)  
            return view_func(request, *args, **kwargs)   
        return _wrapper_irma_authorisation_message
    return decorator_wrapper