# Generated by Django 4.0.6 on 2022-10-09 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_rating_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]