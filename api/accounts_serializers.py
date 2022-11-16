from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.core.cache import cache

from .utils.jwt import get_token_for_user
from accounts.utils import otp_code
from utils.send_email import send_email
from utils.convert_numbers import persian_to_english


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

            trying_count = cache.get(f'{attrs["email"]}-try')
            if not trying_count:
                cache.set(key=f'{attrs["email"]}-try', value=1, timeout=86400)
            else:
                if trying_count > 10:
                    raise serializers.ValidationError(_('limit!! please try 24 hours later.'))
                cache.incr(key=f'{attrs["email"]}-try')

            code = otp_code()

            cache.set(
                key=attrs['email'],
                value={
                    "code": code,
                    "username": attrs['username'],
                    "email": attrs['email'],
                    "password": attrs['password']
                    },
                timeout=120
                )

            send_email(_('OTP Code'), code, [attrs['email']])

        return attrs


class UserVerifyEmailToRegisterSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, min_length=4)
    email = serializers.EmailField(max_length=199)

    def validate(self, attrs):
        if attrs.get('code') and attrs['email']:
            code = persian_to_english(attrs['code'])

            if len(code) != 4:
                raise serializers.ValidationError(_('Invalid code!'))

            if cache.get(f'{attrs["email"]}-try') > 10:
                raise serializers.ValidationError(_('limit!! please try 24 hours later.'))
            cache.incr(key=f'{attrs["email"]}-try')

            info_register = cache.get(key=attrs['email'])

            if not info_register:
                raise serializers.ValidationError(_('Invalid code!'))
            if info_register['code'] != code:
                raise serializers.ValidationError(_('Invalid code!'))

            user = get_user_model().objects.create_user(
                email=info_register['email'],
                password=info_register['password'],
                username=info_register['username']
            )

            token = get_token_for_user(user)
            attrs['token'] = token

        return attrs
