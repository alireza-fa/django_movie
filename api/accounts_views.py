from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .accounts_serializers import TokenJWTSerializer


class TokenJWTView(APIView):
    serializer_class = TokenJWTSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data.get('token'), status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    # TODO: complete this class
    pass
