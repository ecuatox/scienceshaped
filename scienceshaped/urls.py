from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
import authentication
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^projects/', include('projects.urls')),
    url(r'^files/', include('files.urls')),
    url(r'^authentication/', include('authentication.urls')),
    url(r'^login/', views.login, name='login'),
    url(r'^filter/(?P<tag>.*)/', views.index, name='filter'),
    url(r'^aboutEdit', views.aboutEdit, name='about-edit'),
    url(r'^infoEdit', views.infoEdit, name='info-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
