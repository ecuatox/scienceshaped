from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^image/(?P<title>[0-9]+)/$', views.image, name='image'),
    url(r'^images/$', views.images, name='images'),
    url(r'^image-upload/$', views.image_upload, name='image-upload'),
    url(r'^upload-done/$', views.upload_done, name='upload-done'),
]
