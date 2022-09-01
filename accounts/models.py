from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager, AdminManager


class User(AbstractBaseUser):
    Member = 1
    AUTHOR = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (1, _('member')),
        (2, _('author')),
        (3, _('admin'))
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=32, unique=True, verbose_name=_('username'),
        validators=[username_validator],
        error_messages={'unique': _('a user with that username already exists.')})
    email = models.CharField(
        max_length=199, unique=True, verbose_name=_('email'),
        error_messages={'unique': _('a user with that email already exists.')}
    )
    first_name = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('last name'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_admin = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=Member, verbose_name=_('role'))

    default_manager = AdminManager()
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
