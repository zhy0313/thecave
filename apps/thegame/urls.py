urlpatterns = [
    url(r'^$', views.index),
    url(r'register^$', views.register),
    url(r'login^$', views.login),
    url(r'home^$', views.home)
]
