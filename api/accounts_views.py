from rest_framework import status
from django.utils.translation import gettext_lazy as _

from .accounts_serializers import TokenJWTSerializer, UserRegisterSerializer, UserVerifyEmailToRegisterSerializer
from .utils.views import PostView


class TokenJWTView(PostView):
    serializer_class = TokenJWTSerializer
    filter_data_to_response = 'token'


class UserRegisterView(PostView):
    serializer_class = UserRegisterSerializer
    status = status.HTTP_201_CREATED
    filter_data_to_response = 'email'


class UserVerifyEmailTORegisterView(PostView):
    serializer_class = UserVerifyEmailToRegisterSerializer
    status = status.HTTP_200_OK
    filter_data_to_response = 'token'
