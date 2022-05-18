from django.test import TestCase

class NormalFlowTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    # test with authentication session with one attribute. Checks if start_irma_session returns a succesfull 
    # HTTP request (code 200) and if the IRMA server status is "INITIALIZED" 
    def test_register_and_authenticate_pseudonym_anonymous(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym',
        'sessionType' : 'IRMA_register',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/1ofWzImXxNru7chdLzoS\", \"irmaqr\": \"disclosing\"}, \"token\": \"CGXgTgMamPKPnwwT8Ln7\", \"frontendRequest\": {\"authorization\": \"fDUH7ZdmY9OHaleopxFu\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"
        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"CGXgTgMamPKPnwwT8Ln7\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"B9GUh0A5I4s\", \"value\": {\"\": \"B9GUh0A5I4s\", \"en\": \"B9GUh0A5I4s\", \"nl\": \"B9GUh0A5I4s\"}, \"id\": \"pbdf.sidn-pbdf.irma.pseudonym\", \"status\": \"PRESENT\", \"issuancetime\": 1648684800}]]}"
        })

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())
        self.assertIn(
            ('username', 'B9GUh0A5I4s'), 
            response.client.session.items())
        self.assertIn(
            ('firstname', ''), 
            response.client.session.items())
        self.assertIn(
            ('lastname', ''), 
            response.client.session.items())

        self.assertRedirects(response, '/irma/test_succeeded_page/')

        # Authenticate
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym',
        'sessionType' : 'IRMA_authenticate',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/ZH1FVAZ9WyO2UOjXQ7iP\", \"irmaqr\": \"disclosing\"}, \"token\": \"FPuA7Au5Zd9N4e1Mx5KB\", \"frontendRequest\": {\"authorization\": \"FyNCUfa40roIjB2Sq5bc\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"
        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"FPuA7Au5Zd9N4e1Mx5KB\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"B9GUh0A5I4s\", \"value\": {\"\": \"B9GUh0A5I4s\", \"en\": \"B9GUh0A5I4s\", \"nl\": \"B9GUh0A5I4s\"}, \"id\": \"pbdf.sidn-pbdf.irma.pseudonym\", \"status\": \"PRESENT\", \"issuancetime\": 1648684800}]]}"
        })

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())

        self.assertRedirects(response, '/irma/test_succeeded_page/')

    def test_register_and_authenticate_encrypted_pseudonym_and_name(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym&pbdf.gemeente.personalData.initials&pbdf.gemeente.personalData.surname',
        'sessionType' : 'IRMA_encrypted_register',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/WLo2AWzEyKiyVYeydk92\", \"irmaqr\": \"disclosing\"}, \"token\": \"lqcUyCLQVXLre5fXrdfj\", \"frontendRequest\": {\"authorization\": \"9BbXyq9SLQhCknB9WlBV\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"
        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"lqcUyCLQVXLre5fXrdfj\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"B9GUh0A5I4s\", \"value\": {\"\": \"B9GUh0A5I4s\", \"en\": \"B9GUh0A5I4s\", \"nl\": \"B9GUh0A5I4s\"}, \"id\": \"pbdf.sidn-pbdf.irma.pseudonym\", \"status\": \"PRESENT\", \"issuancetime\": 1648684800}, {\"rawvalue\": \"A.B.C.\", \"value\": {\"\": \"A.B.C.\", \"en\": \"A.B.C.\", \"nl\": \"A.B.C.\"}, \"id\": \"pbdf.gemeente.personalData.initials\", \"status\": \"PRESENT\", \"issuancetime\": 1649289600}, {\"rawvalue\": \"Jansen\", \"value\": {\"\": \"Jansen\", \"en\": \"Jansen\", \"nl\": \"Jansen\"}, \"id\": \"pbdf.gemeente.personalData.surname\", \"status\": \"PRESENT\", \"issuancetime\": 1649289600}]]}"
        })

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())
        self.assertRedirects(response, '/irma/test_succeeded_page/')

        # Authenticate

        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym',
        'sessionType' : 'IRMA_encrypted_authenticate',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/ZH1FVAZ9WyO2UOjXQ7iP\", \"irmaqr\": \"disclosing\"}, \"token\": \"FPuA7Au5Zd9N4e1Mx5KB\", \"frontendRequest\": {\"authorization\": \"FyNCUfa40roIjB2Sq5bc\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"
        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"FPuA7Au5Zd9N4e1Mx5KB\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"B9GUh0A5I4s\", \"value\": {\"\": \"B9GUh0A5I4s\", \"en\": \"B9GUh0A5I4s\", \"nl\": \"B9GUh0A5I4s\"}, \"id\": \"pbdf.sidn-pbdf.irma.pseudonym\", \"status\": \"PRESENT\", \"issuancetime\": 1648684800}]]}"
        })

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())
        self.assertNotIn(
            ('username', 'B9GUh0A5I4s'), 
            response.client.session.items())
        self.assertIn(
            ('firstname', 'A.B.C.'), 
            response.client.session.items())
        self.assertIn(
            ('lastname', 'Jansen'), 
            response.client.session.items())

        self.assertRedirects(response, '/irma/test_succeeded_page/')

        # Logout

        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : '',
        'sessionType' : 'IRMA_unauthenticate',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : ''
        })
        response = self.client.get('/irma/perform_irma_session/')

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())
        self.assertRedirects(response, '/irma/test_succeeded_page/')