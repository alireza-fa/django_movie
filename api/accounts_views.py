from rest_framework import status
from django.views.generic.base import View

from .accounts_serializers import TokenJWTSerializer, UserRegisterSerializer, UserVerifyEmailToRegisterSerializer
from .utils.views import PostView
from .utils.permissions import IsNotAuthenticated


class TokenJWTView(PostView):
    serializer_class = TokenJWTSerializer
    filter_data_to_response = 'token'
    permission_classes = [IsNotAuthenticated]


class UserRegisterView(PostView):
    serializer_class = UserRegisterSerializer
    status = status.HTTP_201_CREATED
    filter_data_to_response = 'email'
    permission_classes = [IsNotAuthenticated]


class UserVerifyEmailTORegisterView(PostView):
    serializer_class = UserVerifyEmailToRegisterSerializer
    status = status.HTTP_200_OK
    filter_data_to_response = 'token'
    permission_classes = [IsNotAuthenticated]


class UserLogoutView(View):
    def get(self, request):
        pass


# TODO: user profile
# TODO: Logout
# TODO: Blacklist
