from datetime import timedelta, datetime

from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import Payment
from utils.send_email import send_email
from accounts.models import UserPremium


@receiver(post_init, sender=Payment)
def post_initial(sender, **kwargs):
    print('touch after_initial function')
    if kwargs['instance'].status == 1:
        kwargs['instance'].last_status = 1
    else:
        kwargs['instance'].last_status = 2


@receiver(pre_save, sender=Payment)
def before_save(sender, **kwargs):
    if kwargs['instance'].last_status == 2 and kwargs['instance'].status == 1:
        user_premium = UserPremium.default_manager.filter(user=kwargs['instance'].user)
        if user_premium.exists():
            user_premium = user_premium.first()
            if user_premium.expire_time < datetime.now():
                user_premium.expire_time = datetime.now()
            user_premium.expire_time += timedelta(days=kwargs['instance'].plan.per)
            user_premium.save()

        else:
            UserPremium.objects.create(user=kwargs['instance'].user,
                                       expire_time=datetime.now() + timedelta(days=kwargs['instance'].plan.per))

        send_email(_(f'your plan is submitted'),
                   f'your plan({kwargs["instance"].plan.name}) is submitted',
                   [kwargs['instance'].user.email])
