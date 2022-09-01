from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
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
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
