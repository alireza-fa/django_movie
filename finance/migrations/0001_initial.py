# Generated by Django 3.2 on 2022-10-03 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=34, verbose_name='name')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('per', models.PositiveIntegerField(choices=[(30, 'ماهانه'), (90, 'سه ماهه'), (180, 'شش ماهه'), (365, 'یک ساله')], verbose_name='per')),
                ('best_plan', models.BooleanField(default=False, verbose_name='best plan')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Plans',
            },
        ),
        migrations.CreateModel(
            name='PlanAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_active', models.BooleanField(default=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='finance.plan', verbose_name='plan')),
            ],
            options={
                'verbose_name': 'Plan Attribute',
                'verbose_name_plural': 'Plan Attributes',
            },
        ),
    ]
