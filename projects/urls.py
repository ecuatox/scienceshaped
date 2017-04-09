from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^illustration/(?P<illustration_id>[0-9]+)/edit', views.illustrationEdit, name='illustration-edit'),
    url(r'^illustration/(?P<illustration_id>[0-9]+)/delete', views.illustrationDelete, name='illustration-delete'),
    url(r'^testimonial/(?P<testimonial_id>[0-9]+)/edit', views.testimonialEdit, name='testimonial-edit'),
    url(r'^testimonial/(?P<testimonial_id>[0-9]+)/delete', views.testimonialDelete, name='testimonial-delete'),
]
