# Generated by Django 3.2 on 2022-10-14 01:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_auto_20221008_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 19, 1, 47, 15, 423200), verbose_name='expire time'),
        ),
        migrations.DeleteModel(
            name='UserPlan',
        ),
    ]