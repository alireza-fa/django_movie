from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model

from .utils.jwt import get_token_for_user


class TokenJWTSerializer(serializers.Serializer):
    info_login = serializers.CharField(max_length=199, label=_('username or email'))
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs.get('info_login') and attrs.get('password'):
            user = authenticate(username=attrs.get('info_login'), password=attrs.get('password'))
            if not user:
                raise serializers.ValidationError(_('Not found any user this information.'))
            token = get_token_for_user(user)
            attrs['token'] = token
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def validate(self, attrs):
        if attrs.get('username') and attrs.get('email') and attrs.get('password'):
            # TODO: OTP CODE, SAVING TO CACHE
            attrs['info_register'] = {"email": attrs['email']}
        return attrs
