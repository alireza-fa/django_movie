from datetime import timedelta, datetime

from django.db.models.signals import post_save, pre_save, pre_init, post_init
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import Payment, UserPlan
from utils.send_email import send_email


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
        user_plans = UserPlan.objects.filter(plan=kwargs['instance'].plan)
        if user_plans.exists():
            user_plan = user_plans.first()
            user_plan.expire_time += timedelta(days=kwargs['instance'].plan.per)
            user_plan.save()

        else:
            UserPlan.objects.create(plan=kwargs['instance'].plan,
                                    user=kwargs['instance'].user,
                                    expire_time=datetime.now() + timedelta(days=kwargs['instance'].plan.per))

        send_email(_(f'your plan is submitted'),
                   f'your plan({kwargs["instance"].plan.name}) is submitted',
                   [kwargs['instance'].user.email])
