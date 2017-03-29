from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	
	def register(self, postData):
		errors = []

		if len(postData['first_name']) < 2:
			errors.append('First name must be at least 2 characters long!')
		if len(postData['last_name']) < 2:
			errors.append('Last name must be at least 2 characters long!')
		if not len(postData['email']):
			errors.append('Email field is required!')
		if not EMAIL_REGEX.match(postData['email']):
			errors.append('Email must be valid!')
		if len(postData['password']) < 8:
			errors.append('Password must be at least 8 characters long!')
		if not postData['password'] == postData['confirm_password']:
			errors.append('Paswords must match!')

		user = self.filter(email = postData['email'])

		if user:
			errors.append('Email must be unique!')

		modelResponse = {}

		if errors:
			modelResponse['status'] = False
			modelResponse['errors'] = errors

		else:
			hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

			user = self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed_password)

			modelResponse['status'] = True
			modelResponse['user'] = user

		return modelResponse


	def login(self, postData):
		
		user = self.filter(email = postData['email'])

		modelResponse = {}

		if user:
			if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):

				modelResponse['status'] = True
				modelResponse['user'] = user[0]

			else:
				modelResponse['status'] = False
				modelResponse['error'] = 'Invalid email/password combination!'

		else:
			modelResponse['status'] = False
			modelResponse['error'] = 'Invalid email!'


		return modelResponse

class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()