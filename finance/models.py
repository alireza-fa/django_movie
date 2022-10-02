from django.db import models
from django.utils.translation import gettext_lazy as _


# class Plan(models.Model):
#     MONTH = 1
#     THREE_MONTH = 3
#     SIX_MONTH = 6
#     ONE_YEAR = 1
#
#     PER_CHOICES = (
#         (MONTH, 'یک ماهه'),
#         (THREE_MONTH, 'سه ماهه'),
#         (SIX_MONTH, 'شش ماهه'),
#         (ONE_YEAR, 'یک ساله'),
#     )
#
#     name = models.CharField(max_length=34, verbose_name=_('name'))
#     price = models.PositiveIntegerField(verbose_name=_('price'))
#     is_active = models.BooleanField(default=True, verbose_name=_('is_active'))
#     per = models.PositiveIntegerField(verbose_name=_('per'), )
#     best_plan = models.BooleanField(default=False, verbose_name=_('best plan'))
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
