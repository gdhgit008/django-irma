from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from irma.services import IrmaDjangoSessionManager
import json, requests, hashlib


# Responsible for handling the transformation of data with IRMA.
class IrmaSessionManager:

    def perform_irma_session(request):
        # Restore variables received in start_irma_session
        try:
            session_type = ''
            token = ''
            authorise_attribute_value = ''
            attributes = ''
            request.session['activity_result'] = "FAILURE"
            disclosed_attributes_in_session = True

            if 'session_type' in request.session:
                session_type = request.session['session_type']
            if 'attributes' in request.session:
                attributes = request.session['attributes'] 
            if 'authorisation_value' in request.session:
                authorise_attribute_value = request.session['authorisation_value']
            if 'token' in request.session:
                token = request.session['token']
            
            if IrmaSessionManager.session_type_without_irma_session(request):
                response = ('', 200) 
            else:
                response = IrmaSessionManager.get_response_session_result(request, token)
            irma_proof_status = IrmaSessionManager.get_irma_proof_status(request, response)

            if irma_proof_status == 'VALID':
                if IrmaSessionManager.session_type_without_irma_session(request):
                    disclosed_attributes_in_session = False
                    request.session['activity_result'] = "SUCCESS"
                IrmaSessionManager.perform_irma_action(request, session_type, response, authorise_attribute_value, attributes)
                IrmaDjangoSessionManager.store_disclosed_attributes_in_session(request, response, disclosed_attributes_in_session)
            else:
                disclosed_attributes_in_session = False
            IrmaDjangoSessionManager.store_irmasession_result_in_session(request, session_type, disclosed_attributes_in_session, response)
        except Exception as e:
            print('An error occured during the irma session. ' + 'Exception ' + str(e))

    def perform_irma_action(request, session_type, response, authorise_attribute_value, attributes):
        if session_type == 'IRMA_authenticate' or session_type == 'IRMA_encrypted_authenticate':
            IrmaSessionManager.authenticate_irma_user(request, response, session_type)

        if session_type == 'IRMA_register' or session_type == 'IRMA_encrypted_register':
            IrmaSessionManager.register_irma_user(request, response, session_type)

        if session_type == 'IRMA_authorise':
            IrmaSessionManager.authorise_irma_user(request, response, authorise_attribute_value, attributes)
            
        if session_type == 'IRMA_disclose':
            IrmaSessionManager.disclose_irma_attributes(request)

        if session_type == 'IRMA_unauthenticate':
            IrmaSessionManager.unauthenticate_irma_user(request)
            
        if session_type == 'IRMA_unregister':
            IrmaSessionManager.unregister_irma_user(request)

        if session_type == 'IRMA_clear_authorisations':
            IrmaSessionManager.clear_authorisation_irma_user(request)

        if session_type == 'IRMA_clear_disclose':
            IrmaSessionManager.clear_disclosed_attributes_irma_user(request)

    def get_qrcontent_for_modal(request):
        qrcontent = 'IRMA_session_error'
        if IrmaSessionManager.session_type_without_qr(request):
            qrcontent = "skip"
        else:
            if IrmaSessionManager.session_type_valid(request):
                attributes=request.GET.get('attributes')
                response = IrmaSessionManager.get_response_from_irma_disclosure_post_request(request, attributes)
                if IrmaSessionManager.session_request_succeeded(response):
                    uri = response[0]['sessionPtr']['u']
                    sessionID = uri[uri.rfind('/')+1:len(uri)]
                    token = response[0]['token']
                    IrmaDjangoSessionManager.store_irma_server_response_in_session(request,sessionID, token)
                    # This string is transformed into QRcode in Modal.html
                    qrcontent = "{\"u\":\""+uri+"\",\"irmaqr\":\"disclosing\"}"
                else:
                    if IrmaSessionManager.session_request_failed_IRMA_server_unreachable(response):
                        qrcontent = "IRMA_server_unreachable"
                    else:
                        qrcontent = 'Syntax_error'
            else:
                 qrcontent = 'Syntax_error'
        return qrcontent

    def session_type_without_qr(request):
        return (request.session['session_type'] == 'IRMA_unauthenticate' or 
                request.session['session_type'] == 'IRMA_clear_authorisations' or 
                request.session['session_type'] == 'IRMA_unregister' or 
                request.session['session_type'] == 'IRMA_clear_disclose')

    def session_type_valid(request):
        result = False
        if request.session['session_type'] == 'IRMA_unauthenticate' and request.session['url_next_page'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_clear_authorisations' and request.session['url_next_page'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_unregister' and request.session['url_next_page'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_clear_disclose' and request.session['url_next_page'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_authenticate' and request.session['url_next_page'] is not None and request.session['attributes'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_encrypted_authenticate' and request.session['url_next_page'] is not None and request.session['attributes'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_register' and request.session['url_next_page'] is not None and request.session['attributes'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_encrypted_register' and request.session['url_next_page'] is not None and request.session['attributes'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_disclose' and request.session['url_next_page'] is not None and request.session['attributes'] is not None:
           result = True
        if request.session['session_type'] == 'IRMA_authorise' and request.session['url_next_page'] is not None and request.session['attributes'] is not None and request.session['authorisation_value']:
           result = True
        return result

    def get_response_from_irma_disclosure_post_request(request, attributes):
        if 'test_json_response' in request.session:
            response_json = json.loads(request.session['test_json_response'])
            response_status_code = 200
            del request.session['test_json_response']
        else:
            try:
                if 'test_irma_server' in request.session:
                    session_url = request.session['test_irma_server']
                    del request.session['test_irma_server']
                else:
                    session_url = IrmaSessionManager.build_requestor_session_url()
                json_disclosure_request = IrmaSessionManager.build_json_disclosure_request(attributes)
                headers = {'Authorization': settings.IRMA_SERVER_AUTHENTICATION_TOKEN}
                response = requests.post(session_url, json=json_disclosure_request, headers=headers)
                response_status_code = response.status_code
                response_json = response.json()
            except Exception as e:
                response_status_code = 500
                response_json = ''

        if settings.DEBUG:
            print("Status code: ", response_status_code, "\nresponse server:", response_json)
        return (response_json, response_status_code)   
       

    def build_requestor_session_url():
        irma_server_url = settings.IRMA_SERVER_URL
        irma_server_port = settings.IRMA_SERVER_PORT
        return irma_server_url+':'+irma_server_port+'/session'

    # The internal IRMA inteface allows handling of multiple attributes
    # The IrmaDjangoAPI requests format "attribute1&attribute2"
    # While the IRMA server needs "attribute1","attribute2"
    # First the IRMA-message is build as a JSON String.
    # Then the String is transformed in actual JSON disclosure request format
    def build_json_disclosure_request(attributes):
        attributes_json_string_format = attributes.replace('&', '\",\"')
        session_request_json_string_format = '{ "request": { "@context": "https://irma.app/ld/request/disclosure/v2", "disclose":[[["' + attributes_json_string_format + '"]]] } }'
        return json.loads(session_request_json_string_format)

    def session_request_succeeded(response):
        return response[1] == 200

    def session_request_failed_IRMA_server_unreachable(response):
        return response[1] == 500

    def get_irma_session_status(request):
        # Prepare the GET request to be send to the IRMA server for a session status update
        if 'sessionID' in request.session:
            # only used for testing
            if 'test_IRMA_session_state' in request.session:
                response_json = json.loads(request.session['test_IRMA_session_state'])
                del request.session['test_IRMA_session_state']
                response_status_code = 200
            # normal operations    
            else:
                if 'test_irma_server' in request.session:
                    session_url = request.session['test_irma_server']
                    del request.session['test_irma_server']
                else:
                    sessionID = request.session['sessionID']
                    session_url = IrmaSessionManager.build_irma_session_url()  
                try: 
                    response = requests.get(session_url+sessionID+"/status")
                    response_status_code = response.status_code
                    response_json = response.json()
                except Exception as e:
                    response_status_code = 500
                    response_json = 'IRMA_OFF_LINE'
        else:
            response_status_code = 500
            response_json = 'COOKIE_BLOCKED'

        if settings.DEBUG:
            print("Status code: ", response_status_code, "\nresponse server:", response_json)
        return (response_json, response_status_code)  


    def build_irma_session_url():
        irma_server_url = settings.IRMA_SERVER_URL
        irma_server_port = settings.IRMA_SERVER_PORT
        return irma_server_url+':'+irma_server_port+'/irma/session/'

    def authenticate_irma_user(request, response, session_type):
        try:
            usernamestr = response[0]['disclosed'][0][0]['rawvalue']
            if session_type == 'IRMA_encrypted_authenticate':
                usernamestr = IrmaSessionManager.create_pseudonym_username_string(usernamestr)
            user = authenticate(request, username=usernamestr)
            if 'irma.irma_auth_backend.IrmaAuthenticationBackend' in settings.AUTHENTICATION_BACKENDS:
                user = authenticate(request, username=usernamestr)
                if user is not None:
                    login(request, user)
                    request.session['username'] = usernamestr
                    request.session['firstname'] = user.first_name
                    request.session['lastname'] = user.last_name
                    request.session['activity_result'] = "SUCCESS"
            else:
                raise Exception('\'Settings\' object has no IRMA authentication backend reference')

        #Authentication failure
        except Exception as e:
            print('IRMA_authenticate session failed. ' + 'Exception ' + str(e))

    def register_irma_user(request, response, session_type):
        try:
            first_name = ''
            last_name = ''
            usernamestr = response[0]['disclosed'][0][0]['rawvalue']
            element_count = len(response[0]['disclosed'][0])
            if element_count > 1:
                first_name = response[0]['disclosed'][0][1]['rawvalue']
            if element_count > 2:
                last_name = response[0]['disclosed'][0][2]['rawvalue']
            if session_type == 'IRMA_encrypted_register':
                usernamestr = IrmaSessionManager.create_pseudonym_username_string(usernamestr)
            request.session['username'] = usernamestr
            request.session['firstname'] = first_name
            request.session['lastname'] = last_name
            user = User.objects.create_user(username = usernamestr, password = '')
            if user is not None:
                user.set_unusable_password()
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                request.session['activity_result'] = "SUCCESS"
        #register failure
        except Exception as e:
            print('IRMA_register session failed. ' + 'Exception ' + str(e))

    def authorise_irma_user(request, response, authorise_value, attributes):
        attributes_value = response[0]['disclosed'][0][0]['rawvalue']
        # iteration if more attribute values are disclosed, must have the format result1&result2&...
        if len(response[0]['disclosed'][0]) > 1:
            for index in range(1, len(response[0]['disclosed'][0])):
                attributes_value = attributes_value+'&'+response[0]['disclosed'][0][index]['rawvalue']
        if attributes_value == authorise_value:
            IrmaDjangoSessionManager.store_successful_authorisation_in_session(request, attributes)
        else:
            IrmaDjangoSessionManager.store_unsuccessful_authorisation_in_session(request)
            
    def disclose_irma_attributes(request):
        try:
            request.session['activity_result'] = "SUCCESS"
        except Exception as e:
            print('disclose session failed. ' + 'Exception ' + str(e))

    def unregister_irma_user(request):
        if 'displayed_attributes' in request.session:
            temp1 = request.session['displayed_attributes']
        if 'disclosed_attributes' in request.session:
            temp2 = request.session['disclosed_attributes']
        if 'authorised_attributes' in request.session:
            temp3 = request.session['authorised_attributes']
        if 'activity_result' in request.session:
            temp4 = request.session['activity_result'] 
        username = request.user.username
        logout(request)
        request.session['username'] = ''
        request.session['firstname'] = ''
        request.session['lastname'] = ''
        user_object = User.objects.get(username = username)
        user_object.delete()
        if 'temp1' in locals():
            request.session['displayed_attributes'] = temp1
        if 'temp2' in locals():
            request.session['disclosed_attributes'] = temp2
        if 'temp3' in locals():
            request.session['authorised_attributes'] = temp3
        if 'temp4' in locals():
            request.session['activity_result'] = temp4

    #stores session data in tempo veriables, otherwise data is lost because session is deleted during logout
    def unauthenticate_irma_user(request):
        if 'displayed_attributes' in request.session:
            temp1 = request.session['displayed_attributes']
        if 'disclosed_attributes' in request.session:
            temp2 = request.session['disclosed_attributes']
        if 'authorised_attributes' in request.session:
            temp3 = request.session['authorised_attributes']
        if 'activity_result' in request.session:
            temp4 = request.session['activity_result']    
        logout(request)
        request.session['username'] = ''
        request.session['firstname'] = ''
        request.session['lastname'] = ''
        if 'temp1' in locals():
            request.session['displayed_attributes'] = temp1
        if 'temp2' in locals():
            request.session['disclosed_attributes'] = temp2
        if 'temp3' in locals():
            request.session['authorised_attributes'] = temp3
        if 'temp4' in locals():
            request.session['activity_result'] = temp4

    def clear_authorisation_irma_user(request):
        IrmaDjangoSessionManager.unauthorise_session(request)

    def clear_disclosed_attributes_irma_user(request):
        IrmaDjangoSessionManager.clear_disclosed_attributes_from_session(request)

    def session_type_without_irma_session(request) -> bool:
        return (request.session['session_type'] == 'IRMA_unauthenticate' or 
                request.session['session_type'] == 'IRMA_clear_authorisations' or 
                request.session['session_type'] == 'IRMA_unregister' or 
                request.session['session_type'] == 'IRMA_clear_disclose')

    def get_response_session_result(request, token):
        if 'test_json_response' in request.session:
            response_json = json.loads(request.session['test_json_response'])
            response_status_code = 200
            del request.session['test_json_response']
            return (response_json, response_status_code)
        else:
            if 'test_irma_server' in request.session:
                session_result_url = request.session['test_irma_server']
                del request.session['test_irma_server']
            else:
                session_result_url = settings.IRMA_SERVER_URL+':'+settings.IRMA_SERVER_PORT+'/session/'+token+'/result'
            try: 
                response = requests.get(session_result_url)
                response_status_code = response.status_code
                response_json = response.json()
            except Exception as e:
                response_status_code = 500
                response_json = ''

        if settings.DEBUG:
            print("Status code: ", response_status_code, "\nresponse server:", response_json)
        return (response_json, response_status_code)  

    #This makes the UserId unrelatable to other websites
    def create_pseudonym_username_string(usernamestr):
        hash = hashlib.new('sha256')
        hash.update(str(settings.SECRET_KEY).encode("utf-8"))
        hash.update(usernamestr.encode("utf-8"))
        return hash.hexdigest()

    #Some session types (unauthenticate, unregister etc) do not require a irma session and get a valid status
    def get_irma_proof_status(request, response):
        status = 'INVALID'
        if IrmaSessionManager.session_type_without_irma_session(request):
            status = 'VALID'
        else:
            if IrmaSessionManager.session_request_succeeded(response):
                status = response[0]['proofStatus']
        return status