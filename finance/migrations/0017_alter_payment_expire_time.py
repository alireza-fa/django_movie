# Generated by Django 3.2 on 2022-12-07 22:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0016_alter_payment_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 12, 22, 7, 42, 414538), verbose_name='expire time'),
        ),
    ]
