from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^illustration/(?P<illustration_id>[0-9]+)/$', views.illustration, name='illustration'),
    # url(r'^illustrations/$', views.illustrations, name='illustrations'),
    url(r'^illustration/(?P<illustration_id>[0-9]+)/edit', views.illustrationEdit, name='illustration-edit'),
]
