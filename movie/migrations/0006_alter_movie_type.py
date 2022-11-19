# Generated by Django 3.2 on 2022-10-03 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20220927_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'فیلم'), (2, 'سریال')], default=1, verbose_name='type'),
        ),
    ]