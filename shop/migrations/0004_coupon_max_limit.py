# Generated by Django 4.0.6 on 2022-09-21 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_coupon_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='max_limit',
            field=models.IntegerField(default=0),
        ),
    ]
