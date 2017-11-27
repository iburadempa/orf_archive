from django.conf.urls import url
from django.contrib.auth.views import login
from . import views


urlpatterns = [
    url(r'^login/?$', login, {'template_name': 'login.html'}, name='orf_archive_login'),
    url(r'^index/?$', views.index, name='index'),
    url(r'^day/(?P<day>[-0-9]{10})/?$', views.day, name='day'),
    url(r'^files/oe1/[0-9]{4}-[0-9]{2}-[0-9]{2}/(?P<filename>.*)/?$', views.download, name='download'),
]
