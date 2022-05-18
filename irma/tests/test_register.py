from django.test import TestCase

class RegistrationTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    # Test with normal registration session with one attribute. Checks if start_irma_session returns a succesfull 
    # HTTP request (code 200) and if the IRMA server status is "INITIALIZED" 
    # Successfull normal anonymous registration
    def test_normal_register_pseudonym_anonymous(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym',
        'sessionType' : 'IRMA_register',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : ''
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/irma/get_irma_session_status/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual( str(response.content, encoding='utf8'), {'status' : 'INITIALIZED'})

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

    # Test with normal registration session with three attributes. 
    # Successfull normal registration with fullname
    def test_normal_register_pseudonym_fullname(self):

        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym&pbdf.gemeente.personalData.initials&pbdf.gemeente.personalData.surname',
        'sessionType' : 'IRMA_register',
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
        self.assertIn(
            ('username', 'B9GUh0A5I4s'), 
            response.client.session.items())
        self.assertIn(
            ('firstname', 'A.B.C.'), 
            response.client.session.items())
        self.assertIn(
            ('lastname', 'Jansen'), 
            response.client.session.items())
        self.assertRedirects(response, '/irma/test_succeeded_page/')

    # Test with registration session with three attributes. 
    # Successfull encrypted registration with fullname
    def test_encrypted_register_pseudonym_anonymous(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym',
        'sessionType' : 'IRMA_encrypted_register',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : ''
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/irma/get_irma_session_status/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual( str(response.content, encoding='utf8'), {'status' : 'INITIALIZED'})

        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"CGXgTgMamPKPnwwT8Ln7\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"B9GUh0A5I4s\", \"value\": {\"\": \"B9GUh0A5I4s\", \"en\": \"B9GUh0A5I4s\", \"nl\": \"B9GUh0A5I4s\"}, \"id\": \"pbdf.sidn-pbdf.irma.pseudonym\", \"status\": \"PRESENT\", \"issuancetime\": 1648684800}]]}"
        })

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())
        self.assertNotIn(
            ('username', 'B9GUh0A5I4s'), 
            response.client.session.items())
        self.assertIn(
            ('firstname', ''), 
            response.client.session.items())
        self.assertIn(
            ('lastname', ''), 
            response.client.session.items())
        self.assertRedirects(response, '/irma/test_succeeded_page/')

    # Test with encrypted registration session with three attributes. 
    # Successfull encrypted registration with fullname
    def test_encrypted_register_pseudonym_fullname(self):

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

    # Test with normal registration session with one non-existing attribute.
    # HTTP request (code 200) and if the IRMA server status is "INITIALIZED" 
    # Unsuccessfull normal anonymous registration
    def test_normal_register_pseudonym_anonymous_incorrect(self):
        response = self.client.get('/irma/start_irma_session/', 
            { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudo',
            'sessionType' : 'IRMA_register',
            'urlNextPage' : '/irma/test_succeeded_page/',
            'authorisationValue' : ''
            })
        self.assertEqual(
            response.json()['qrcontent'],
            'Syntax_error')
    # Test with normal registration session with one existing and one non-existing attribute.
    # Unsuccessfull normal anonymous registration
    def test_normal_register_pseudonym_anonymous_incorrect_two(self):
        response = self.client.get('/irma/start_irma_session/', 
             { 'attributes' : 'pbdf.sidn-pbdf.irma.pseudonym&',
               'sessionType' : 'IRMA_register',
               'urlNextPage' : '/irma/test_succeeded_page/',
               'authorisationValue' : ''
             })
        self.assertEqual(
            response.json()['qrcontent'],
            'Syntax_error')

