# Generated by Django 3.2 on 2022-12-03 21:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0015_alter_payment_expire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 8, 21, 39, 18, 564180), verbose_name='expire time'),
        ),
    ]
