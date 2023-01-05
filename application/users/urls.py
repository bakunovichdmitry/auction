from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SignUpView

urlpatterns = [
    path('auth/jwt-token/', TokenObtainPairView.as_view(), name='jwt_token'),
    path('auth/base-token/', obtain_auth_token, name='base_token'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
]
