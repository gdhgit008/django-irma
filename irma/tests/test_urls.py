from django.test import TestCase

class YourTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    # test with disclosure session with one attribute. Checks if start_irma_session returns a succesfull 
    # HTTP request (code 200) and if the IRMA server status is "INITIALIZED" 
    def test_disclosure_session_one_attribute(self):
        response = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.gemeente.personalData.fullname',
        'sessionType' : 'IRMA_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : ''
        })
        response_status = self.client.get('/irma/get_irma_session_status/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_status.status_code, 200)
        self.assertJSONEqual( str(response_status.content, encoding='utf8'), {'status' : 'INITIALIZED'})

    def test_disclosure_session_two_attributes(self):
        response_two_attributes = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.gemeente.personalData.fullname&pbdf.gemeente.address.street',
        'sessionType' : 'IRMA_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : ''
        })
        response_status = self.client.get('/irma/get_irma_session_status/')
        self.assertEqual(response_two_attributes.status_code, 200)
        self.assertEqual(response_status.status_code, 200)
        self.assertJSONEqual( str(response_status.content, encoding='utf8'), {'status' : 'INITIALIZED'})

    def test_disclosure_session_multiple_attributes(self):
        response_multiple_attributes = self.client.get('/irma/start_irma_session/', 
        { 'attributes' : 'pbdf.gemeente.personalData.fullname&pbdf.gemeente.address.street&pbdf.gemeente.address.houseNumber&pbdf.gemeente.address.zipcode&pbdf.gemeente.address.city',
        'sessionType' : 'IRMA_disclose',
        'urlNextPage' : '/irma/test_succeeded_page/',
        'authorisationValue' : 'Yes'
        })
        response_status = self.client.get('/irma/get_irma_session_status/')
        self.assertEqual(response_multiple_attributes.status_code, 200)
        self.assertEqual(response_status.status_code, 200)
        self.assertJSONEqual( str(response_status.content, encoding='utf8'), {'status' : 'INITIALIZED'})