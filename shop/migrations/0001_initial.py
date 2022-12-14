# Generated by Django 4.0.6 on 2022-09-04 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(blank=True, upload_to='static/banners')),
                ('title', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('is_select', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('url_slug', models.CharField(max_length=200, null=True)),
                ('thumbnail', models.FileField(default=0, upload_to='static')),
                ('description', models.TextField(max_length=250)),
                ('category_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=250, null=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('discount_price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField()),
                ('descriptions', models.CharField(max_length=500)),
                ('thumbnail', models.CharField(max_length=200)),
                ('image1', models.ImageField(blank=True, null=True, upload_to='static')),
                ('image2', models.ImageField(blank=True, upload_to='static')),
                ('image3', models.ImageField(blank=True, upload_to='static')),
                ('is_available', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
            ],
        ),
    ]
