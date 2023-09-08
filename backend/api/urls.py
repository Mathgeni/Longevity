from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.views.users import UserRegisterView, UserLoginView, VerifyOTP, UserView

app_name = 'api'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('verify/', VerifyOTP.as_view(), name='verify'),
    path('user/', UserView.as_view(), name='user'),
]

