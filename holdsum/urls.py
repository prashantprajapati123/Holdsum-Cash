from django.conf.urls import include, url
from django.contrib import admin

from accounts.views import FacebookLogin


urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('accounts.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
