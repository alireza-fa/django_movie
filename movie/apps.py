from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MovieConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie'
    verbose_name = _('Movie Config')
