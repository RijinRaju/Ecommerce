# Generated by Django 4.0.6 on 2022-09-28 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_product_offer_offer_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='category_offer',
            name='offer_percent',
            field=models.IntegerField(default=0),
        ),
    ]
