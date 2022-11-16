from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import accounts_views


app_name = 'api'


accounts_urls = [
    path('register/', accounts_views.UserRegisterView.as_view(), name='register'),
    path('register/verify_email/', accounts_views.UserVerifyEmailTORegisterView.as_view(),
         name='register_verify_email')
]


urlpatterns = [
    path('token/', accounts_views.TokenJWTView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #
    path('accounts/', include(accounts_urls)),
]
