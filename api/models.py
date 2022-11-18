from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class OutstandingToken(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('user')
    )

    jti = models.CharField(unique=True, max_length=255, verbose_name=_('jti'))
    token = models.TextField(verbose_name=_('token'))

    created_at = models.DateTimeField(verbose_name=_('created at'))
    expire_time = models.DateTimeField(verbose_name=_('expire time'))

    class Meta:
        verbose_name = _('Outstanding Token')
        verbose_name_plural = _('Outstanding Tokens')
        ordering = ("user",)

    def __str__(self):
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )


class BlacklistedToken(models.Model):
    token = models.OneToOneField(OutstandingToken, on_delete=models.CASCADE, verbose_name=_('token'))

    blacklisted_at = models.DateTimeField(auto_now_add=True, verbose_name=_('blacklist at'))

    class Meta:
        verbose_name = _('Blacklist Token')
        verbose_name_plural = _('Blacklist Tokens')

    def __str__(self):
        return f"Blacklisted token for {self.token.user}"
