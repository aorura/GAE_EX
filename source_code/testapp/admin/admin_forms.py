#!/usr/bin/env python
# encoding: utf-8
"""
admin_forms.py

Created by Jason Elbourne on 2012-02-03.
Copyright (c) 2012 Jason Elbourne. All rights reserved.
"""

from wtforms import Form, TextField, TextAreaField, BooleanField, validators


class WaitingListForm(Form):
	email = TextField(u'Email', validators=[validators.required()])
	company = TextField(u'Company')
	founder = BooleanField(u'Founder?')
	
	def validate_company(form, field):
		founder = form.founder.data
		if founder:
			if not field.data:
				raise validators.ValidationError('If you are Founder, Company Domain is Required')