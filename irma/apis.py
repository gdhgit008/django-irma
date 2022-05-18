from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from irma.services import IrmaDjangoSessionManager
from irma.interfaces import IrmaSessionManager
from irma.decorators import irma_authorisation_required

# This class is the access point of the IRMA Django API.
# The public functions available for Django Developers are in this class.
class IrmaApi:
    # Stores and sends the JSON data to Modal.html for QR display or inline IRMA app
    def start_irma_session(request):
        IrmaDjangoSessionManager.store_test_variables_in_session(request)
        IrmaDjangoSessionManager.store_request_variables_in_session(request)
        return IrmaApi._get_initial_modal_json_response(request)

    # Modal.html requests periodically a status update from IRMA server.
    # Send the status in JSON format back to Modal.html
    def get_irma_session_status(request):
        IrmaDjangoSessionManager.store_test_variables_in_session(request)
        return IrmaApi._get_irma_session_status_json_response(request)

    # Possible actions:
    # IRMA_authenticate: disclose attribute + user database lookup returns user object
    # IRMA_encrypted_authenticate: disclose attribute + encryption + user database lookup returns user object
    # IRMA_register: disclose attribute + create user in database returns null (login later)
    # IRMA_encrypted_register: disclose attribute + encryption + create user in database returns null (login later)
    # Disclose: disclose attribute returns attribute
    # Verify: disclose attribute + anonymous user returns anymous user
    def perform_irma_session(request):
        try:
            url_next_page = request.session['url_next_page']
        except Exception as e:
            print('No URL next page specified. ' + 'Exception ' + str(e))   
        IrmaDjangoSessionManager.store_test_variables_in_session(request)      
        IrmaSessionManager.perform_irma_session(request)
        return redirect(url_next_page)

    # ------------ API helpers
    def _get_initial_modal_json_response(request):
        qrcontent = IrmaSessionManager.get_qrcontent_for_modal(request)
        device_type = IrmaApi._get_device_type(request)
        if settings.DEBUG:
            print('Device type: '+device_type)
            print('QRcontent: ' + qrcontent )
        modal_json_response = {
            'qrcontent' : qrcontent,
            'device_type' : device_type
        }
        return JsonResponse(modal_json_response) 

    def _get_irma_session_status_json_response(request):
        response = IrmaSessionManager.get_irma_session_status(request)
        data = {
            'status' : response[0]
        }
        return JsonResponse(data)

    # device_type is relevant for Modal.html to determine whether an
    # Qrcode should be displayed or in case of mobile user an
    # inline IRMA app should be started
    def _get_device_type(request):
        device_type = 'unknown'
        if request.user_agent.is_pc:
            device_type = 'pc'
        if request.user_agent.is_mobile:
            device_type = 'mobile'
        return device_type

    # Required for test purposes
    def test_succeeded_page(request):
        return JsonResponse({'Test': 'Succeeded'})

    # Required for test purposes
    @irma_authorisation_required('pbdf.gemeente.personalData.over18','','')
    def test_authorisation_page(request):
        return JsonResponse({'Authorisation': 'Succeeded'})