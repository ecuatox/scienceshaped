from django.conf.urls import url
from .views import edit, new, delete, name

urlpatterns = [
    url(r'^edit/$', edit, name='edit'),
    url(r'^edit/name/(?P<name>.*)/$', name, name='edit-name'),
    url(r'^(?P<group_id>[0-9]+)/edit/$', edit, name='edit'),
    url(r'^delete/(?P<tag_id>[0-9]+)/$', delete, name='delete'),
    url(r'^(?P<group_id>[0-9]+)/edit/new/$', new, name='new'),
]
