from django.shortcuts import render, redirect, HttpResponse
from .models import Item, User
from django.contrib import messages

# Create your views here.
def index(request):
	user = User.objects.get(id=request.session['user_id'])
	context = {
		"items" : Item.objects.exclude(user=user).exclude(wishlist__id=request.session['user_id']),
		"user" : User.objects.get(id=request.session['user_id']),
		"users" : User.objects.filter(id=request.session['user_id']),
		"user_items" : Item.objects.filter(user=user)| Item.objects.filter(wishlist__id=request.session['user_id']),
		
	}

	# request.session[''] = user.id

	return render(request, 'newapp/index.html', context)

def newitem(request):
	context = {
		"users" : User.objects.all()
	}

	return render(request, 'newapp/add.html', context)

def additem(request):

	response_from_models = Item.objects.additem(request.POST, request.session['user_id'])
	
	if request.method =='POST':
		if response_from_models['status']:
			return redirect('newapp:index')
		else:
			for error in response_from_models['errors']:
				messages.error(request, error)

			return redirect("newapp:newitem")

def addwishlist(request, id):
	response_from_models = Item.objects.addwishlist(request.POST, request.session['user_id'], id)


	# clear = Item.objects.get(id=id).delete()
	return redirect('newapp:index')

def item(request, id):
	context = {
		"items" : Item.objects.get(id=id)
	}
	return render(request, 'newapp/item.html', context)

def delete(request, id):
	response_from_models = Item.objects.delete(request.POST, id)

	return redirect("newapp:index")

def remove(request, id):

	response_from_models = Item.objects.remove(request.POST, request.session['user_id'], id)

	return redirect("newapp:index")
	





