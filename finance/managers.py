from django.db.models import Manager

from datetime import datetime


class IsActiveManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class IsActiveAndValidExpireTimeManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, expire_time__gte=datetime.now())
