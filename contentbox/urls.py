from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<title>.*)/edit', views.contentbox, name='contentbox'),
]
