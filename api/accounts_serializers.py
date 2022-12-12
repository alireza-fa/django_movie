from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.core.cache import cache

from movie.models import Movie
from .movie_serializer import MovieListSerializer, MovieReviewSerializer
from .utils.jwt import get_token_for_user
from accounts.utils import otp_code
from accounts.models import UserPasswordReset
from utils.send_email import send_email
from utils.convert_numbers import persian_to_english
from .models import OutstandingToken, BlacklistedToken

from datetime import datetime


class TokenJWTSerializer(serializers.Serializer):
    info_login = serializers.CharField(max_length=199, label=_('username or email'))
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
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
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
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


class UserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutstandingToken
        fields = ('token', )

    def validate(self, attrs):
        try:
            token = RefreshToken(token=attrs['token'])

        except TokenError:
            raise serializers.ValidationError(_('Token is invalid or expired.'))

        finally:
            user = self.context['request'].user

            if OutstandingToken.objects.filter(jti=token.get('jti'), user=user).exists():
                raise serializers.ValidationError(_('Token is invalid or expired.'))

            iat = datetime.fromtimestamp(token.get('iat'))
            exp = datetime.fromtimestamp(token.get('exp'))

            outstanding = OutstandingToken.objects.create(
                user=user, jti=token.get('jti'),
                token=str(token), created_at=iat, expire_time=exp
            )

            BlacklistedToken.objects.create(token=outstanding)

        return attrs


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        try:
            token = RefreshToken(token=attrs['refresh'])
        except TokenError:
            raise serializers.ValidationError(_('Token is invalid or expired.'))

        if BlacklistedToken.objects.filter(token__token=str(token)).exists():
            raise serializers.ValidationError(_('Token is invalid or expired.'))

        attrs['access_token'] = {"access": str(token.access_token)}

        return attrs


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=128)
    new_password = serializers.CharField(min_length=8, max_length=128)

    def validate(self, attrs):
        request = self.context['request']
        user = authenticate(username=request.user.username, password=attrs['old_password'])
        if not user:
            raise serializers.ValidationError(_('old password is wrong.'))
        user.set_password(attrs['new_password'])
        user.save()
        return attrs


class UserForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=199)

    def validate_email(self, email):
        user = get_user_model().objects.filter(email=email)
        if user.exists():
            resets = UserPasswordReset.objects.filter(user=user[0])
            if resets.count() >= 3:
                raise serializers.ValidationError(_('You reach the limit reset email (three time per one day)'))
            reset = UserPasswordReset.objects.create(user=user[0])
            send_email(
                subject=_('Reset password'),
                body=f'for reset password, enter the blow link:\n{reset.get_absolute_url()}',
                receiver_list=[email])
        return email


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=128)

    def validate(self, attrs):
        user = self.context['reset'].user
        user.set_password(attrs['password'])
        user.save()
        self.context['reset'].delete()
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    recommend_movies = serializers.SerializerMethodField(method_name='get_recommend_movie', read_only=True)
    last_reviews = serializers.SerializerMethodField(method_name='get_last_reviews', read_only=True)
    comment_count = serializers.SerializerMethodField(method_name='get_comment_count', read_only=True)
    review_count = serializers.SerializerMethodField(method_name='get_review_count', read_only=True)
    plan_days = serializers.SerializerMethodField(method_name='get_plan_days', read_only=True)
    favorite_movies = serializers.SerializerMethodField(method_name='get_favorite_movies', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name',
                  'recommend_movies', 'last_reviews',
                  'comment_count', 'review_count',
                  'plan_days', 'favorite_movies',)
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def get_recommend_movie(self, obj):
        movies = Movie.get_recommend_movie(user=obj)
        return MovieListSerializer(instance=movies, many=True).data

    def get_last_reviews(self, obj):
        reviews = obj.get_last_reviews()
        return MovieReviewSerializer(instance=reviews, many=True).data

    def get_comment_count(self, obj):
        return obj.get_comments().count()

    def get_review_count(self, obj):
        return obj.get_reviews().count()

    def get_plan_days(self, obj):
        return obj.get_plan_days()

    def get_favorite_movies(self, obj):
        movies = Movie.objects.filter(favorites__user=obj)
        return MovieListSerializer(instance=movies, many=True).data


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
