from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import accounts_views


app_name = 'api'


accounts_urls = [
    path('register/', accounts_views.UserRegisterView.as_view(), name='register'),
    path('register/verify_email/', accounts_views.UserVerifyEmailTORegisterView.as_view(),
         name='register_verify_email'),
    path('logout/', accounts_views.UserLogoutView.as_view(), name='user_logout'),
]


urlpatterns = [
    path('token/', accounts_views.TokenJWTView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/refresh/verify/', TokenVerifyView.as_view(), name='refresh_verify'),
    # path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    #
    path('accounts/', include(accounts_urls)),
]
