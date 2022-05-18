from django.test import TestCase

class AuthorisationTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    # Test with Authoristion session with one attribute. 
    # First access is denied
    # Second access is granted
    def test_authorisation(self):
        response = self.client.get('/irma/test_authorisation_page')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.gemeente.personalData.over18',
        'sessionType' : 'IRMA_authorise',
        'urlNextPage' : '/irma/test_authorisation_page/',
        'authorisationValue' : 'Yes',
        'test_json_response' : "{\"sessionPtr\": {\"u\": \"https://www.someserver.com:8088/irma/session/03RrY7t1qMOzICjD06Q5\", \"irmaqr\": \"disclosing\"}, \"token\": \"tcLhxrpy9OQijqx9NPyC\", \"frontendRequest\": {\"authorization\": \"90pj10WGhsBlXDl8a4P3\", \"minProtocolVersion\": \"1.0\", \"maxProtocolVersion\": \"1.1\"}}"
        })
        response = self.client.get('/irma/perform_irma_session/', 
        { 'test_json_response' : "{\"token\": \"tcLhxrpy9OQijqx9NPyC\", \"status\": \"DONE\", \"type\": \"disclosing\", \"proofStatus\": \"VALID\", \"disclosed\": [[{\"rawvalue\": \"Yes\", \"value\": {\"\": \"Yes\", \"en\": \"Yes\", \"nl\": \"Yes\"}, \"id\": \"pbdf.gemeente.personalData.over18\", \"status\": \"PRESENT\", \"issuancetime\": 1649289600}]]}"
        })

        self.assertIn(
            ('activity_result', 'SUCCESS'), 
            response.client.session.items())

        self.assertRedirects(response, '/irma/test_authorisation_page/')