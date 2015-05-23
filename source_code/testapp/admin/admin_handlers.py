import webapp2
import logging

from testapp import basehandler
from testapp.waitinglist import waitinglist_models as wl_models

import admin_forms as forms

from google.appengine.api import users


class AdminPageHandler(basehandler.BaseHandler):
	def get(self):
		if users.is_current_user_admin():

			user = users.get_current_user()
			logout_url = users.create_logout_url("/admin")
			waitinglist = wl_models.WaitingList.get()
			add_waitinglist_action = webapp2.uri_for('admin_add_waitinglist', _full=True)
			delete_waitinglist_action = webapp2.uri_for('admin_delete_waitinglist', _full=True)

			context = {
						'user': user, \
						'logout_url': logout_url, \
						'waitinglist': waitinglist, \
						'add_waitinglist_action': add_waitinglist_action, \
						'delete_waitinglist_action': delete_waitinglist_action, \
						'form_add_waitinglist': self.form, \
						}

			self.render_response('admin/admin.html', **context)

		else:
			login_url = users.create_login_url("/admin")

			context = {'login_url': login_url}

			self.render_response('admin/login.html', **context)


	@webapp2.cached_property
	def form(self):
		try:
			return forms.WaitingListForm(self.request.POST)
		except Exception, e:
			logging.error('_testapp Error - ADMIN - AdminPageHandler(FORM) - %s' % str(e))
			self.abort(403)


class AddWaitinglistHandler(basehandler.BaseHandler):
	def post(self):
		if self.form.validate():
			
			email = self.form.email.data
			company = self.form.company.data
			founder = self.form.founder.data

			added = wl_models.WaitingList.set(email, company, founder)
			
			if added:
				self.add_message(u"You (%s) have been added to the Waiting List" % str(email), "success")
				logging.info('_testapp Debug - Email (%s) added to Waiting List' % str(email))
			else:
				self.add_message(u"Error adding the Email Address (%s) to the waiting List." % \
					str(email), 'error')
				logging.error('_testapp Debug - ERROR User NOT added to Waiting List')

		# Form Not Valid
		for field, errors in self.form.errors.items():
			for error in errors:
				self.add_message(u"Error in the %s field - %s" % (
					getattr(self.form, field).label.text,
					error
				), 'error')

		self.redirect(webapp2.uri_for('admin_page', _full=True))

	@webapp2.cached_property
	def form(self):
		try:
			return forms.WaitingListForm(self.request.POST)
		except Exception, e:
			logging.error('_testapp Error - ADMIN - AddWaitinglistHandler(FORM) - %s' % str(e))
			self.abort(403)


class DeleteWaitinglistHandler(basehandler.BaseHandler):
	def post(self):
			
		user_email = self.request.get('user_email', None)
		
		if user_email:
			wl_models.WaitingList.delete(user_email)
			self.add_message(u"Email (%s) been deleted from the Waiting List" % str(user_email), "success")
			logging.info('_testapp Debug - Email (%s) deleted from Waiting List' % str(user_email))
		else:
			self.add_message(u"Error deleting the Email Address (%s) from the waiting List." % str(user_email), 'error')
			logging.error('_testapp Debug - ERROR User (%s) NOT deleted from Waiting List' % str(user_email))


		self.redirect(webapp2.uri_for('admin_page', _full=True))
