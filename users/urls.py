from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', obtain_auth_token, name='base_token'),
    path('jwt/token/', TokenObtainPairView.as_view(), name='jwt_token'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]