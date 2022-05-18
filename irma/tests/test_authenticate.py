from django.test import TestCase

class AuthenticationTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        # Register encrypted with pseudonym full name
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
        
        #Register Normal pseudonym anonymous
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


    def tearDown(self):
        # Clean up run after every test method.
        pass

    # Test with normal authentication session with one attribute. 
    # Successfull normal authentication
    def test_normal_authenticate_pseudonym_anonymous(self):

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
        self.assertIn(
            ('username', 'B9GUh0A5I4s'), 
            response.client.session.items())
        self.assertRedirects(response, '/irma/test_succeeded_page/')


    # Test with encrypted authentication session with one attribute. 
    # Successfull encrypted authentication
    def test_encrypted_authenticate_pseudonym_fullname(self):

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
        self.assertRedirects(response, '/irma/test_succeeded_page/')

    # Test with normal authentication session with one attribute. 
    # Unsuccessfull normal authentication
    def test_normal_authenticate_pseudonym_anonymous_failure(self):

        # Authenticate
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym',
        'sessionType' : 'IRMA_authenticate',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/ZH1FVAZ9WyO2UOjXQ7iP\", \"irmaqr\": \"disclosing\"}, \"token\": \"FPuA7Au5Zd9N4e1Mx5KB\", \"frontendRequest\": {\"authorization\": \"FyNCUfa40roIjB2Sq5bc\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"
        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"FPuA7Au5Zd9N4e1Mx5KB\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"B9GUh0A5I4t\", \"value\": {\"\": \"B9GUh0A5I4t\", \"en\": \"B9GUh0A5I4t\", \"nl\": \"B9GUh0A5I4t\"}, \"id\": \"pbdf.sidn-pbdf.irma.pseudonym\", \"status\": \"PRESENT\", \"issuancetime\": 1648684800}]]}"
        })

        self.assertIn(
            ('activity_result', 'FAILURE'), 
            response.client.session.items())

        self.assertRedirects(response, '/irma/test_succeeded_page/')


    # Test with encrypted authentication session with one attribute. 
    # Unsuccessfull encrypted authentication
    def test_encrypted_authenticate_pseudonym_fullname_failure(self):

        # Authenticate
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym',
        'sessionType' : 'IRMA_encrypted_authenticate',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : '',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/ZH1FVAZ9WyO2UOjXQ7iP\", \"irmaqr\": \"disclosing\"}, \"token\": \"FPuA7Au5Zd9N4e1Mx5KB\", \"frontendRequest\": {\"authorization\": \"FyNCUfa40roIjB2Sq5bc\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"
        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"FPuA7Au5Zd9N4e1Mx5KB\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"B9GUh0A5I4t\", \"value\": {\"\": \"B9GUh0A5I4t\", \"en\": \"B9GUh0A5I4t\", \"nl\": \"B9GUh0A5I4t\"}, \"id\": \"pbdf.sidn-pbdf.irma.pseudonym\", \"status\": \"PRESENT\", \"issuancetime\": 1648684800}]]}"
        })

        self.assertIn(
            ('activity_result', 'FAILURE'), 
            response.client.session.items())
        
        self.assertRedirects(response, '/irma/test_succeeded_page/')