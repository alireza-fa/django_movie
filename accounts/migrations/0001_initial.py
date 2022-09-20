# Generated by Django 3.2 on 2022-09-17 09:53

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_delete', models.BooleanField(blank=True, editable=False, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('username', models.CharField(error_messages={'unique': 'a user with that username already exists.'}, max_length=32, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(error_messages={'unique': 'a user with that email already exists.'}, max_length=199, unique=True, verbose_name='email')),
                ('first_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'کاربر'), (2, 'نویسنده'), (3, 'ادمین')], default=1, verbose_name='role')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
