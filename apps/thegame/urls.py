from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'enter$', views.enter),
    url(r'cave$', views.cave),
    url(r'action$', views.action),
    url(r'logout$', views.logout),
    url(r'lost$', views.lost),
    url(r'home$', views.home)
]
