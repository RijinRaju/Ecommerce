# Generated by Django 4.0.6 on 2022-09-26 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_delete_return_expiary'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='exp_date',
            field=models.DateTimeField(null=True),
        ),
    ]
