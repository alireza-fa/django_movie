from django.contrib import admin

from .models import Magazine


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    search_fields = ('email',)
