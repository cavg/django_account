from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list', views.list, name='account-list'),
    url(r'^me', views.me, name='account-me'),
    url(r'^users', views.users, name='account-users'),
    url(r'^new', views.new, name='account-new'),
]