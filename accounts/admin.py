from django.contrib import admin

from .models import UserPremium, UserPasswordReset


@admin.register(UserPremium)
class UserPremiumAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserPasswordReset)
