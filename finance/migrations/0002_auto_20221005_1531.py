# Generated by Django 3.2 on 2022-10-05 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(0, 'Zarinpal'), (1, 'Saman'), (2, 'Sepehr'), (3, 'Wallet')], max_length=32, verbose_name='name')),
                ('data_auth', models.TextField(blank=True, null=True, verbose_name='data auth')),
                ('api_request', models.CharField(blank=True, max_length=240, null=True, verbose_name='api request')),
                ('api_verify', models.CharField(blank=True, max_length=240, null=True, verbose_name='api verify')),
                ('callback_url', models.CharField(blank=True, max_length=240, null=True, verbose_name='callback url')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Gateway',
                'verbose_name_plural': 'Gateways',
            },
        ),
        migrations.AlterModelManagers(
            name='plan',
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wallet', to=settings.AUTH_USER_MODEL, verbose_name='wallet')),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': 'Wallets',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid_field', models.UUIDField(db_index=True, default=uuid.UUID('2cc5e751-7bd6-432a-8cd7-68f1e159f8dc'), unique=True, verbose_name='uuid field')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
                ('authority', models.CharField(blank=True, max_length=250, null=True, verbose_name='authority')),
                ('ref_id', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Paid'), (2, 'Not paid')], default=2, verbose_name='status')),
                ('need_checkout', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='finance.gateway', verbose_name='gateway')),
                ('plan', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.plan', verbose_name='plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]