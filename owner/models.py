from django.db import models
from django.http import request

# Create your models here.


class Owner(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True,max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class monthly_sales_report(models.Model):
    date = models.DateField(null=True)
    product_name = models.CharField(null=True, max_length=100)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
