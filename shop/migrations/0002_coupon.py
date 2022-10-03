# Generated by Django 4.0.6 on 2022-09-21 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now=True)),
                ('valid_until', models.DateTimeField()),
                ('coupon_code', models.CharField(max_length=20)),
                ('maximum_discount_amount', models.IntegerField()),
                ('is_redeem', models.BooleanField(default=False)),
            ],
        ),
    ]
