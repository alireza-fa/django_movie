import uuid
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models, transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .managers import IsActiveManager, IsActiveAndValidExpireTimeManager
from .gateways import zarinpal


class Plan(models.Model):
    MONTH = 30
    THREE_MONTH = 90
    SIX_MONTH = 180
    ONE_YEAR = 365

    PER_CHOICES = (
        (MONTH, 'ماهانه'),
        (THREE_MONTH, 'سه ماهه'),
        (SIX_MONTH, 'شش ماهه'),
        (ONE_YEAR, 'یک ساله'),
    )

    name = models.CharField(max_length=34, verbose_name=_('name'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    is_active = models.BooleanField(default=True, verbose_name=_('is_active'))
    per = models.PositiveIntegerField(choices=PER_CHOICES, verbose_name=_('per'))
    best_plan = models.BooleanField(default=False, verbose_name=_('best plan'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        verbose_name = _('Plan')
        verbose_name_plural = _('Plans')

    def __str__(self):
        return self.name

    def get_price(self):
        discount = self.get_discount()
        if discount:
            discount_amount = (self.price * discount.discount) // 100
            return int(self.price) - discount_amount
        return self.price

    def get_discount(self):
        return self.discounts.filter(expire_time__gte=datetime.now()).order_by('-discount').first()


class PlanAttribute(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='attributes', verbose_name=_('plan'))
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Plan Attribute')
        verbose_name_plural = _('Plan Attributes')

    def __str__(self):
        return f'{self.plan} - {self.name}'


class PlanDiscount(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='discounts', verbose_name=_('plan'))
    discount = models.IntegerField(
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(100)], verbose_name=_('discount')
    )
    expire_time = models.DateTimeField(verbose_name=_('expire time'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Plan Discount')
        verbose_name_plural = _('Plan Discounts')

    def __str__(self):
        return f'{self.plan} - {self.discount}'


# class UserPlan(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='plans', verbose_name=_('user'))
#     plan = models.ForeignKey(Plan, on_delete=models.RESTRICT, related_name='users', verbose_name=_('plan'))
#     expire_time = models.DateTimeField(verbose_name=_('expire time'))
#     is_active = models.BooleanField(default=True, verbose_name=_('is active'))
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     default_manager = models.Manager()
#     objects = IsActiveAndValidExpireTimeManager()
#
#     class Meta:
#         verbose_name = _('User Plan')
#         verbose_name_plural = _('User Plans')
#
#     def __str__(self):
#         return f'{self.user} - {self.plan.name} - is active: {self.is_active}'


class Gateway(models.Model):
    ZARINPAL = 1
    SAMAN = 2
    SEPEHR = 3
    WALLET = 4

    NAME_CHOICES = (
        (ZARINPAL, _('Zarinpal')),
        (SAMAN, _('Saman')),
        (SEPEHR, _('Sepehr')),
        (WALLET, _('Wallet'))
    )

    GATEWAY_FUNCTION = {
        ZARINPAL: {
            "send_request": zarinpal.send_request,
            "verify": zarinpal.verify
        },
        SAMAN: {
            "send_request": '',
            "verify": ''
        },
        SEPEHR: {
            "send_request": '',
            "verify": ''
        },
        WALLET: {
            "send_request": '',
            "verify": ''
        }
    }

    name = models.PositiveSmallIntegerField(verbose_name=_('name'), choices=NAME_CHOICES)
    data_auth = models.TextField(verbose_name=_('data auth'), null=True, blank=True)
    api_request = models.CharField(max_length=240, verbose_name=_('api request'), null=True, blank=True)
    api_verify = models.CharField(max_length=240, verbose_name=_('api verify'), null=True, blank=True)
    callback_url = models.CharField(max_length=240, verbose_name=_('callback url'), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        verbose_name = _('Gateway')
        verbose_name_plural = _('Gateways')

    def __str__(self):
        return self.get_name_display()

    def request_handler(self, payment):
        function = self.get_request_function()
        data = {
            "merchant": self.data_auth,
            "amount": payment.price,
            "callback_url": self.callback_url,
            "description": payment.plan.name,
            "api_request": self.api_request,
            "mobile": '09309806535',
            "email": payment.user.email,
        }
        return function(**data)

    def get_request_function(self):
        return self.GATEWAY_FUNCTION[self.name].get('send_request')

    def verify_handler(self, payment, request):
        function = self.get_verify_function()
        if function:
            data = {
                "request": request,
                "merchant": self.data_auth,
                "amount": payment.price,
                "authority": payment.authority,
                "api_verify": self.api_verify,
            }
            return function(**data)

    def get_verify_function(self):
        return self.GATEWAY_FUNCTION[self.name].get('verify')


class Payment(models.Model):
    PAID = 1
    NOT_PAID = 2

    STATUS_CHOICES = (
        (PAID, _('Paid')),
        (NOT_PAID, _('Not paid')),
    )

    uuid_field = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name=_('uuid field'))
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                             verbose_name=_('user'), related_name='payments')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL,
                             null=True, verbose_name=_('plan'), related_name='payments')
    gateway = models.ForeignKey(Gateway, on_delete=models.PROTECT,
                                related_name=_('payments'), verbose_name=_('gateway'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    authority = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('authority'))
    ref_id = models.CharField(max_length=250, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=NOT_PAID, verbose_name=_('status'))
    logs = models.TextField(verbose_name=_('logs'), null=True, blank=True)
    need_check = models.BooleanField(default=False, verbose_name=_('need check'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    expire_time = models.DateTimeField(default=datetime.now() + timedelta(days=5), verbose_name=_('expire time'))

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    default_manager = models.Manager()
    objects = IsActiveAndValidExpireTimeManager()

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return f'{self.uuid_field} - {self.get_status_display()}'

    @classmethod
    def create(cls, user, plan_id, gateway_id):
        plan = get_object_or_404(Plan.objects.all(), id=plan_id)
        gateway = get_object_or_404(Gateway.objects.all(), id=gateway_id)
        if plan and gateway:
            payment = cls(user=user, plan=plan, gateway=gateway, price=plan.get_price())
            plan_discount = plan.get_discount()
            if plan_discount:
                payment.expire_time = plan_discount.expire_time
            payment.save()
            return payment

    def get_link_request(self):
        status, data = self.gateway.request_handler(self)
        if status == 100:
            self.authority = data['authority']
            self.logs = f'code is 200, authority: {self.authority}, time: {datetime.now()}'
            self.save()
            return data['url']
        else:
            self.logs = f'error code is: {data["error_code"]}' \
                        f', message code is: {data["error_message"]} ' \
                        f', time: {datetime.now()}\n'
            self.save()
            return None

    def verify(self, request):
        status, data = self.gateway.verify_handler(payment=self, request=request)
        if status and data:
            if status == 100:
                with transaction.atomic(using='main_db'):
                    self.status = self.PAID
                    self.ref_id = data['ref_id']
                    self.logs += f'\ncode: {status}, message: success, ref_id: {self.ref_id}, time: {datetime.now()}'
                    self.save()

            elif status == 101:
                with transaction.atomic(using='main_db'):
                    self.status = 1
                    self.logs += f'\ncode: {status}, message: {data["message"]}, time: {datetime.now()}'
                    self.save()

            else:
                self.logs += f'\nerror code: {status}, message error: {data["message"]}, time: {datetime.now()}'

            return status, data

        self.logs += f'\nerror or canceled via client, time: {datetime.now()}'
        self.save()
        return status, data
