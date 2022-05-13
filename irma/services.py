from django.conf import settings

# Responsible for the logic around coordination and transactions with Django Sessions.
class IrmaDjangoSessionManager:

    # Store the received JSON parameters from Modal.html in the 
    # session for later use. This is the way to keep paramters
    # available in the procedures get_irma_session_status and perform_irma_session
    def store_request_variables_in_session(request):
        request.session['session_type'] = request.GET.get('sessionType')
        request.session['url_next_page'] = request.GET.get('urlNextPage')
        request.session['attributes'] = request.GET.get('attributes')
        request.session['authorisation_value'] = request.GET.get('authorisationValue')   

    # Store test information in Django session
    def store_test_variables_in_session(request):
        if request.GET.get('test_json_response'):
            request.session['test_json_response'] = request.GET.get('test_json_response')
        if request.GET.get('test_irma_server'):
            request.session['test_irma_server'] = request.GET.get('test_irma_server')
        if request.GET.get('test_IRMA_session_state'):
            request.session['test_IRMA_session_state'] = request.GET.get('test_IRMA_session_state')

    # Store information from the IRMA server response in Django session
    def store_irma_server_response_in_session(request, sessionID, token):
        request.session['sessionID'] = sessionID
        request.session['token'] = token

    def store_irmasession_result_in_session(request, session_type, disclosed_attributes_in_session, response):
        session_result_string = ('{"activity_type": "' + session_type + '", "activity_result": "' +
                            request.session['activity_result'] +'"')
        if disclosed_attributes_in_session:
            for attribute in response[0]['disclosed'][0]:
                session_result_string = session_result_string + ',"' +attribute['id']+'": "' +attribute['rawvalue']+'"'
        session_result_json = (session_result_string + '}').replace('\'', '\"')
        if settings.DEBUG:
            print("Session result: " + session_result_json)
        request.session['session_result'] = session_result_json

    def store_disclosed_attributes_in_session(request, response, disclosed_attributes_in_session):
        if disclosed_attributes_in_session:
            if  not 'disclosed_attributes' in request.session:
                request.session['disclosed_attributes'] = {}
            for index in response[0]['disclosed'][0]:
                request.session['disclosed_attributes'][index['id']] = index['rawvalue']
    
    def store_successful_authorisation_in_session(request, attributes):
        # If it is first verify action create an empty list in the session
        if not 'authorised_attributes' in request.session:
            request.session['authorised_attributes'] = {}
        # Add the disclosed attributes to the 'is_authorised' list
        # This info is later used in decorators.py
        attribute_list = attributes.split('&')
        for attribute in attribute_list:
            request.session['authorised_attributes'][attribute] = True       
        request.session.set_expiry(0)
        request.session['activity_result'] = "SUCCESS"
        request.session['authorisation_failed'] = False
    
    def store_unsuccessful_authorisation_in_session(request):
        request.session['authorisation_failed'] = True
    
    def unauthorise_session(request):
        if 'displayed_attributes' in request.session:
            request.session['displayed_attributes'] = []
        if 'authorised_attributes' in request.session:
            request.session['authorised_attributes'] = {}
        request.session['authorisation_removed'] = True

    def clear_disclosed_attributes_from_session(request):
        if 'disclosed_attributes' in request.session:
            request.session['disclosed_attributes'] = {}    
        request.session['disclosed_attributes_removed'] = True