# Generated by Django 3.2 on 2022-10-14 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220927_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPremium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_time', models.DateTimeField(verbose_name='expire time')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='premium', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'User premium',
                'verbose_name_plural': 'User Premiums',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
