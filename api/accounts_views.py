from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView
from django.contrib.auth import get_user_model

from .accounts_serializers import (TokenJWTSerializer, UserRegisterSerializer, UserVerifyEmailToRegisterSerializer,
                                   UserLogoutSerializer, TokenRefreshSerializer, UserChangePasswordSerializer,
                                   UserForgetPasswordSerializer, UserResetPasswordSerializer, UserProfileSerializer,
                                   UserProfileEditSerializer,)
from accounts.models import UserPasswordReset
from .utils.views import PostView
from .utils.permissions import IsNotAuthenticated, ProfilePermission


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


class UserChangePasswordView(PostView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserChangePasswordSerializer
    send_request_to_serializer = True
    message_to_response = 'your password successfully changed.'


class UserForgetPasswordView(PostView):
    serializer_class = UserForgetPasswordSerializer
    message_to_response = 'if entered your email is a correct email, we sent a mail for reset password.'


class UserResetPasswordView(APIView):
    serializer_class = UserResetPasswordSerializer

    def get(self, request, uuid):
        reset = get_object_or_404(UserPasswordReset, uuid=uuid)
        serializer = self.serializer_class(data=request.data, context={"reset": reset})
        serializer.is_valid(raise_exception=True)
        return Response(data={"data": 'Your password successfully changed.'})


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = (ProfilePermission,)
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserProfileEditSerializer
