import unittest
import webtest

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

from testapp.waitinglist import waitinglist_models as wl_models
from testapp.message import mail_handlers

from main import app

class testappTestCase(unittest.TestCase):

	def setUp(self):
		
		self.testapp = webtest.TestApp(app)
        
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Create a consistency policy that will simulate the High Replication consistency model.
		self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
		# Initialize the datastore stub with this policy.
		self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
		# Initialize the mail stub
		self.testbed.init_mail_stub()
		self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)


	def tearDown(self):
		self.testbed.deactivate()
		
##############################################################################
##############################################################################
##############################################################################
##############################################################################


	def test__WaitingListEntity(self):
		email = 'test@test.com'
	
		test_model = wl_models.WaitingList

		wl = test_model(email=str(email))
		key = wl.put()

		wl2 = key.get()

		self.assertEqual('test@test.com', wl2.email)
		
		try:
			wl = test_model()
			key = wl.put()
			works = True
		except:
			works = False

		self.assertFalse(works)


	def test__MailSent(self):
		email = 'test@test.com'
		
		mail_handlers.AddedToWaitingListMessage.send_email(email)
		
		messages = self.mail_stub.get_sent_messages(to=email)
		
		self.assertEqual(1, len(messages))
		self.assertEqual('test@test.com', messages[0].to)


	def test__HomeHandler(self):
		response = self.testapp.get('/')

		self.assertEqual(response.status_int, 200)
		self.assertEqual(response.content_type, 'text/html')


	def test__AdminHandler(self):
		response = self.testapp.get('/admin')

		self.assertEqual(response.status_int, 200)
		self.assertEqual(response.content_type, 'text/html')





if __name__ == '__main__':
	unittest.main()