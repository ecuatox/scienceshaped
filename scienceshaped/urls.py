from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
import authentication
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^projects/', include('projects.urls')),
    url(r'^files/', include('files.urls')),
    url(r'^authentication/', include('authentication.urls')),
    url(r'^login/', views.login, name='login'),
    url(r'^filter/(?P<tag>.*)/', views.index, name='filter'),
]
