from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .accounts_serializers import (TokenJWTSerializer, UserRegisterSerializer, UserVerifyEmailToRegisterSerializer,
                                   UserLogoutSerializer, TokenRefreshSerializer,
                                   )
from .utils.views import PostView
from .utils.permissions import IsNotAuthenticated


class TokenJWTView(PostView):
    serializer_class = TokenJWTSerializer
    filter_data_to_response = 'token'
    permission_classes = (IsNotAuthenticated, )


class UserRegisterView(PostView):
    serializer_class = UserRegisterSerializer
    status = status.HTTP_201_CREATED
    filter_data_to_response = 'email'
    permission_classes = (IsNotAuthenticated, )


class UserVerifyEmailTORegisterView(PostView):
    serializer_class = UserVerifyEmailToRegisterSerializer
    status = status.HTTP_200_OK
    filter_data_to_response = 'token'
    permission_classes = (IsNotAuthenticated, )


class UserLogoutView(PostView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserLogoutSerializer
    status = status.HTTP_204_NO_CONTENT
    send_request_to_serializer = True
    no_content = True


class TokenRefreshView(PostView):
    serializer_class = TokenRefreshSerializer
    filter_data_to_response = 'access_token'
    status = status.HTTP_200_OK


# TODO: user profile
# TODO: search
# TODO: Checking blacklist before create access token or authentication refresh token (str(token.access_token_class))
