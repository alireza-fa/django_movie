# Generated by Django 3.2 on 2022-10-05 17:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0007_auto_20221005_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 10, 17, 5, 45, 971002), verbose_name='expire time'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='finance.plan', verbose_name='plan'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='uuid_field',
            field=models.UUIDField(db_index=True, default=uuid.UUID('163cc09e-58c2-4d50-90e4-aef9125a1fc0'), unique=True, verbose_name='uuid field'),
        ),
    ]
