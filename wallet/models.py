from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.SET_NULL,
        related_name=_('wallet'), verbose_name=_('wallet'), null=True
    )

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def __str__(self):
        return f'{self.user.username} - {self.pk}'


class TransactionWallet(models.Model):
    RECEIVE = 1
    GIVE = -1

    TYPE_CHOICES = (
        (RECEIVE, _('Receive')),
        (GIVE, _('Give'))
    )

    wallet = models.ForeignKey(
        Wallet, on_delete=models.PROTECT,
        related_name=_('transactions'), verbose_name=_('wallet'))
    type = models.SmallIntegerField(choices=TYPE_CHOICES, verbose_name=_('type'))
    amount = models.PositiveIntegerField(verbose_name=_('amount'))
