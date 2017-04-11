from django.contrib.auth.decorators import permission_required
from django.conf.urls import url

from .views import IllustrationEdit, illustrationDelete, TestimonialEdit, testimonialDelete

urlpatterns = [
    url(r'^illustration/(?P<illustration_id>[0])/edit/$', permission_required(('projects.add_illustration'))(IllustrationEdit.as_view()), name='illustration-add'),
    url(r'^illustration/(?P<illustration_id>[0-9]+)/edit/$', permission_required(('projects.change_illustration'))(IllustrationEdit.as_view()), name='illustration-edit'),
    url(r'^illustration/(?P<illustration_id>[0-9]+)/delete/$', illustrationDelete, name='illustration-delete'),
    url(r'^testimonial/(?P<testimonial_id>[0])/edit/$', permission_required(('projects.add_testimonial'))(TestimonialEdit.as_view()), name='testimonial-edit'),
    url(r'^testimonial/(?P<testimonial_id>[0-9]+)/edit/$', permission_required(('projects.edit_testimonial'))(TestimonialEdit.as_view()), name='testimonial-edit'),
    url(r'^testimonial/(?P<testimonial_id>[0-9]+)/delete/$', testimonialDelete, name='testimonial-delete'),
]
