from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^newitem$', views.newitem, name="newitem"),
    url(r'^additem$', views.additem, name="additem"),
    url(r'^addwishlist/(?P<id>\d+)$', views.addwishlist, name='addwishlist'),
    url(r'^item/(?P<id>\d+)$', views.item, name='item'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
     url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
     url(r'^/(?P<id>\d+)$', views.delete, name='delete'),


]
