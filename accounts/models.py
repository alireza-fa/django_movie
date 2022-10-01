from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager, AdminManager, SoftDeleteManager


class SoftDelete(models.Model):
    is_delete = models.BooleanField(null=True, blank=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.deleted_at = timezone.now()
        self.save()

    deleted = SoftDeleteManager()


class User(AbstractBaseUser, SoftDelete):
    Member = 1
    AUTHOR = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (1, 'کاربر'),
        (2, 'نویسنده'),
        (3, 'ادمین')
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=32, unique=True, verbose_name=_('username'),
        validators=[username_validator],
        error_messages={'unique': _('a user with that username already exists.')})
    email = models.EmailField(
        max_length=199, unique=True, verbose_name=_('email'),
        error_messages={'unique': _('a user with that email already exists.')}
    )
    first_name = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('last name'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=Member, verbose_name=_('role'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    default_manager = AdminManager()
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    def has_perm(self, perms, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.role == 3:
            return True
        return False

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('panel:user_edit', args=[self.pk])
