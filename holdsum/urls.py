from django.conf.urls import include, url
from django.contrib import admin

from accounts.views import FacebookLogin, LoginView


urlpatterns = [
    url(r'^auth/login/', LoginView.as_view(), name='login'),
    url(r'^auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('accounts.urls')),
    url(r'^transaction/', include('transactions.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
