# Generated by Django 3.2 on 2022-11-18 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            name='TransactionWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(1, 'Receive'), (-1, 'Give')], verbose_name='type')),
                ('amount', models.PositiveIntegerField(verbose_name='amount')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='wallet.wallet', verbose_name='wallet')),
            ],
        ),
    ]
