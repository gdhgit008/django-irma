from django.test import TestCase
from django.conf import settings

class testingSettings(TestCase):
	
	def setup(self):
		# Setup run before every test method.
		pass

	def tearDown(self):
		# Clean up run after every test method.
		pass

	def test_settings_variables_set(self):
		self.assertTrue(hasattr(settings, 'IRMA_SERVER_URL'), 'IRMA_SERVER_URL not specified in settings.py')
		self.assertTrue(hasattr(settings, 'IRMA_SERVER_PORT'), 'IRMA_SERVER_PORT not specified in settings.py')
		self.assertTrue(hasattr(settings, 'IRMA_SERVER_AUTHENTICATION_TOKEN'), 'IRMA_SERVER_AUTHENTICATION_TOKEN not specified in settings.py')
		self.assertTrue(hasattr(settings, 'AUTHORISATION_FAILURE'), 'AUTHORISATION_FAILURE not specified in settings.py')
		self.assertTrue(hasattr(settings, 'AUTHORISATION_REMOVED'), 'AUTHORISATION_REMOVED not specified in settings.py')
		self.assertTrue(hasattr(settings, 'AUTHORISATION_PARTIAL'), 'AUTHORISATION_PARTIAL not specified in settings.py')