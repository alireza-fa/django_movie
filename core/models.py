from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))
    email = models.EmailField(max_length=120, verbose_name=_('email'))
    subject = models.CharField(max_length=120, verbose_name=_('subject'))
    body = models.TextField(verbose_name=_('body'))
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Magazine(models.Model):
    email = models.EmailField(max_length=120, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Magazine')
        verbose_name_plural = _('Magazines')

    def __str__(self):
        return self.email
