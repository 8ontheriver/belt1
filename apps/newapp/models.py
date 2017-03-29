from __future__ import unicode_literals

from django.db import models
from ..logreg.models import User

# Create your models here.

class UserManager(models.Manager):
	def additem(self, postData, id):

		errors = []
		print postData
		if len(postData['specificitem']) < 1:
			errors.append("Must include an item!")

		if len(postData['specificitem']) < 3:
			errors.append("Must be at least 3 characters long!")

		items = self.filter(name = postData['specificitem'])
		print items
		if items:
			errors.append("Item is already in the wish list!")
		
		selected_user = User.objects.get(id=id)

		modelResponse = {}

		if errors:
			modelResponse['status'] = False
			modelResponse['errors'] = errors

		else:
			items = Item.objects.create(name=postData['specificitem'], user=selected_user)

			modelResponse['status'] = True
			modelResponse['items'] = items

		return modelResponse

	def addwishlist(self, postData, user_id, id):
		
		item = self.get(id=id)
		user = User.objects.get(id=user_id)
		item.wishlist.add(user)

	def delete(self, postData, id):

		item = self.get(id=id).delete()

	def remove(self, postData, user_id, id):
		
		item = self.get(id=id)
		user = User.objects.get(id=user_id)
		item.wishlist.remove(user)

	
		


class Item(models.Model):
	name = models.CharField(max_length=255)
	user = models.ForeignKey(User, related_name="items_users")
	wishlist = models.ManyToManyField(User, related_name="wish_list")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	objects = UserManager()

	