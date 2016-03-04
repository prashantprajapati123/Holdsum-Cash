from django.conf.urls import include, url
from misc.views import FacebookLogin

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'', include(admin.site.urls)),
]
