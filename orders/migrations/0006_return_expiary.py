# Generated by Django 4.0.6 on 2022-09-26 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderproduct_product_return'),
    ]

    operations = [
        migrations.CreateModel(
            name='Return_expiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
