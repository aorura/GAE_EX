#!/usr/bin/env python
# encoding: utf-8
"""
mail_handlers.py

Created by Jason Elbourne on 2012-02-04.
Copyright (c) 2012 Jason Elbourne. All rights reserved.
"""
import logging
import datetime
import webapp2

from google.appengine.api import mail


NOW = datetime.datetime.now()
ADMIN_EMAIL = 'test@test.com'


class AddedToWaitingListMessage(object):
	
	@classmethod
	def send_email(self, email):
		try:
			mail.send_mail(sender="testapp <%s>" % ADMIN_EMAIL,
						  to=str(email),
						  subject="testapp Notification (Added to Waiting List)",
						  body="""
					Your email address was recently entered into an online form at testapp.com.

					The form entered your email into a Waiting List to be notified when testapp
					is open to the public.

					If this does not sound familiar to you, simply delete this message.

					PRIVILEGED AND CONFIDENTIAL
					This transmission may contain privileged, proprietary or confidential
					information. If you are not the intended recipient, you are instructed not to
					review this transmission. If you are not the intended recipient, please notify
					the sender that you received this message and delete this transmission from your
					system.

					©%d testapp All Rights Reserved.

					""" % (NOW.year)
					)
			logging.info('_testapp - Email was sent (AddedToWaitingListMessage)')
			return True
		
		except Exception, e:
			logging.error('_testapp - Error sending Email message (AddedToWaitingListMessage)')
			return False


class SendMessageTotestapp(object):

	@classmethod
	def send_email(self, name, city, email, message):
		try:
			mail.send_mail(sender="testapp <%s>" % ADMIN_EMAIL,
						  to="testapp <%s>" % ADMIN_EMAIL,
						  subject="testapp Notification (Contact Form Submission)",
						  body="""
						Hello Admin:

						%s has send you a message:
						
						%s

						Name: %s

						City:  %s
						
						Email: %s

						©%d testapp All Rights Reserved.

					""" % (str(name), str(message), str(name), str(city), str(email), NOW.year)
					)

			logging.info('_testapp - Email was sent (SendMessageTotestapp)')
			return True

		except Exception, e:
			logging.error('_testapp - Error sending Email message (SendMessageTotestapp)')
			return False

