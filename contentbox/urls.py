from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from .views import ContentBoxEdit

urlpatterns = [
    url(r'^(?P<title>.*)/edit', permission_required(('contentbox.add_contentbox', 'contentbox.change_contentbox'))(ContentBoxEdit.as_view()), name='contentbox'),
]
