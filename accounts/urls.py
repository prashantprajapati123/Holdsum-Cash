from django.conf.urls import include, url


from .views import PlaidTokenView,UserRegistrationViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'sign-up', UserRegistrationViewSet, base_name='user_sign_up')



urlpatterns = [
	url('', include(router.urls)),
    
]
