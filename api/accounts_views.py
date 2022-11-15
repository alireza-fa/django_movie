from rest_framework import status

from .accounts_serializers import TokenJWTSerializer, UserRegisterSerializer
from .utils.views import PostView


class TokenJWTView(PostView):
    serializer_class = TokenJWTSerializer
    filter_data_to_response = 'token'


class UserRegisterView(PostView):
    serializer_class = UserRegisterSerializer
    status = status.HTTP_201_CREATED


class UserVerifyEmailTORegisterView(PostView):
    # TODO:
    pass
