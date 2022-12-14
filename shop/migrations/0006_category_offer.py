# Generated by Django 4.0.6 on 2022-09-23 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_coupon_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now=True)),
                ('valid_until', models.DateField()),
                ('offer_amount', models.IntegerField(default=0)),
                ('is_Active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
        ),
    ]
