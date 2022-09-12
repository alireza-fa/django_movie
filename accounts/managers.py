from django.contrib.auth.models import BaseUserManager
from django.db.models import Q
from django.utils import timezone
from django.db.models import QuerySet, Manager


class SoftQueryset(QuerySet):
    def delete(self):
        return self.update(is_delete=True, deleted_at=timezone.now())


class SoftManager(BaseUserManager):
    def get_queryset(self):
        return SoftQueryset(model=self.model, using='main_db').filter(Q(is_delete=False) | Q(is_delete__isnull=True))


class AdminManager(SoftManager):
    def create_user(self, email=None, password=None, username=None, first_name=None, last_name=None):
        if email is None:
            raise ValueError('User must have email')
        if username is None:
            raise ValueError('User Must have username')
        user = self.model(username=username, first_name=first_name, last_name=last_name)
        email = self.normalize_email(email)
        user.email = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.role = 3
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserManager(AdminManager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(is_active=True), Q(is_delete=False) | Q(is_delete__isnull=True))


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=True)
