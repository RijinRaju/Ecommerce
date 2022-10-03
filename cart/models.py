from django.db import models
from customers.models import Customers
from shop.models import Products
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    user = models.ForeignKey(Customers,on_delete=models.CASCADE ,null=True,blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    is_Active = models.BooleanField(default=True)
    total = models.IntegerField(default=0 ,null=True)
    dis_amt = models.IntegerField(default=0,null=True)


    def item_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


class Cart_eg(models.Model):
    pid = models.IntegerField(null=True)
    uid = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    total = models.FloatField(null=True,default=0)