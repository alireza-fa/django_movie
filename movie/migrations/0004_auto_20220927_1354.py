# Generated by Django 3.2 on 2022-09-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20220925_1655'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moviereview',
            options={'ordering': ('-created',), 'verbose_name': 'Movie Review', 'verbose_name_plural': 'Movie Reviews'},
        ),
        migrations.AddField(
            model_name='moviecomment',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='is read'),
        ),
        migrations.AddField(
            model_name='moviereview',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='is read'),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='slidermovie',
            name='title',
            field=models.CharField(max_length=64, verbose_name='title'),
        ),
    ]
