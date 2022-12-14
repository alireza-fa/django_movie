# Generated by Django 3.2 on 2022-10-05 15:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_auto_20221005_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateway',
            name='name',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Zarinpal'), (2, 'Saman'), (3, 'Sepehr'), (4, 'Wallet')], verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='uuid_field',
            field=models.UUIDField(db_index=True, default=uuid.UUID('5a91983d-25fe-4b23-b6b3-617c9a955654'), unique=True, verbose_name='uuid field'),
        ),
    ]
