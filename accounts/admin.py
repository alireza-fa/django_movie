from django.contrib import admin

from .models import UserPremium


@admin.register(UserPremium)
class UserPremiumAdmin(admin.ModelAdmin):
    pass
