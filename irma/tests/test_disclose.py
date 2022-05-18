from django.test import TestCase

class DisclosureTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_disclosure_session_one_attribute(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.mobilenumber.mobilenumber',
        'sessionType' : 'IRMA_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/P3bT1o0ielaUBBzV9YzG\", \"irmaqr\": \"disclosing\"}, \"token\": \"woWEqPedWQ26L2MIEbpF\", \"frontendRequest\": {\"authorization\": \"PR9lWytQwDZWCqNedu40\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"

        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"woWEqPedWQ26L2MIEbpF\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"+31612345678\", \"value\": {\"\": \"+31612345678\", \"en\": \"+31612345678\", \"nl\": \"+31612345678\"}, \"id\": \"pbdf.sidn-pbdf.mobilenumber.mobilenumber\", \"status\": \"PRESENT\", \"issuancetime\": 1649894400}]]}"})

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())
        
        self.assertIn(
            ('disclosed_attributes', {'pbdf.sidn-pbdf.mobilenumber.mobilenumber': '+31612345678'}), 
            response.client.session.items())
        
        self.assertRedirects(response, '/irma/test_succeeded_page/')

        # Disclose additional attributes

        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.gemeente.personalData.fullname&pbdf.gemeente.address.street&pbdf.gemeente.address.houseNumber&pbdf.gemeente.address.zipcode&pbdf.gemeente.address.city',
        'sessionType' : 'IRMA_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/UOuM2YIQP7tKIDejkueG\", \"irmaqr\": \"disclosing\"}, \"token\": \"S6TVlaWgqmiUl8Jyzje5\", \"frontendRequest\": {\"authorization\": \"bW3sXgUJFDR9CWzBlVCo\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"

        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"S6TVlaWgqmiUl8Jyzje5\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"A.B.C. Jansen\", \"value\": {\"\": \"A.B.C. Jansen\", \"en\": \"A.B.C. Jansen\", \"nl\": \"A.B.C. Jansen\"}, \"id\": \"pbdf.gemeente.personalData.fullname\", \"status\": \"PRESENT\", \"issuancetime\": 1649289600}, {\"rawvalue\": \"Straatnaam\", \"value\": {\"\": \"Straatnaam\", \"en\": \"Straatnaam\", \"nl\": \"Straatnaam\"}, \"id\": \"pbdf.gemeente.address.street\", \"status\": \"PRESENT\", \"issuancetime\": 1649289600}, {\"rawvalue\": \"8\", \"value\": {\"\": \"8\", \"en\": \"8\", \"nl\": \"8\"}, \"id\": \"pbdf.gemeente.address.houseNumber\", \"status\": \"PRESENT\", \"issuancetime\": 1649289600}, {\"rawvalue\": \"1234 AB\", \"value\": {\"\": \"1234 AB\", \"en\": \"1234 AB\", \"nl\": \"1234 AB\"}, \"id\": \"pbdf.gemeente.address.zipcode\", \"status\": \"PRESENT\", \"issuancetime\": 1649289600}, {\"rawvalue\": \"Plaatsnaam\", \"value\": {\"\": \"Plaatsnaam\", \"en\": \"Plaatsnaam\", \"nl\": \"Plaatsnaam\"}, \"id\": \"pbdf.gemeente.address.city\", \"status\": \"PRESENT\", \"issuancetime\": 1649289600}]]}"})

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())
        
        self.assertIn(
            ('disclosed_attributes', {'pbdf.sidn-pbdf.mobilenumber.mobilenumber': '+31612345678', 'pbdf.gemeente.personalData.fullname': 'A.B.C. Jansen', 'pbdf.gemeente.address.street': 'Straatnaam', 'pbdf.gemeente.address.houseNumber': '8', 'pbdf.gemeente.address.zipcode': '1234 AB', 'pbdf.gemeente.address.city': 'Plaatsnaam'}), 
            response.client.session.items())

        self.assertRedirects(response, '/irma/test_succeeded_page/')
        
        # Undisclose attributes

        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : '',
        'sessionType' : 'IRMA_clear_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : ''
        })
        response = self.client.get('/irma/perform_irma_session/') 
        
        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())
        
        self.assertIn(
            ('disclosed_attributes', {}), 
            response.client.session.items())
        self.assertRedirects(response, '/irma/test_succeeded_page/')


    def test_disclosure_session_no_IRMA_response_1(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.mobilenumber.mobilenumber',
        'sessionType' : 'IRMA_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_irma_server' : 'https://someserver.com'

        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual( str(response.content, encoding='utf8'), {'qrcontent': 'IRMA_server_unreachable', 'device_type': 'unknown'})

    def test_disclosure_session_no_IRMA_response_2(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.mobilenumber.mobilenumber',
        'sessionType' : 'IRMA_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : ''

        })
        response = self.client.get('/irma/get_irma_session_status/',
        {
            'test_irma_server' : 'https://someserver.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual( str(response.content, encoding='utf8'), {'status' : 'IRMA_OFF_LINE'})




    def test_disclosure_session_no_IRMA_response_3(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.mobilenumber.mobilenumber',
        'sessionType' : 'IRMA_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/P3bT1o0ielaUBBzV9YzG\", \"irmaqr\": \"disclosing\"}, \"token\": \"woWEqPedWQ26L2MIEbpF\", \"frontendRequest\": {\"authorization\": \"PR9lWytQwDZWCqNedu40\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"

        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_irma_server' : 'https://someserver.com'
        })

        self.assertIn(
            ('activity_result', 'FAILURE'), 
            response.client.session.items())
        self.assertEqual(response.status_code, 302)