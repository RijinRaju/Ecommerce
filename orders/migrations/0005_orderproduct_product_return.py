# Generated by Django 4.0.6 on 2022-09-24 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='product_return',
            field=models.BooleanField(default=False),
        ),
    ]
