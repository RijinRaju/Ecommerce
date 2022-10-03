from django.db import models
from customers.models import Customers
from shop.models import Products
# Create your models here.


class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=150,blank=True)

    def __str__(self):
        return self.wishlist_id


class WishlistItem(models.Model):
    user = models.ForeignKey(Customers,on_delete=models.CASCADE,null=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE,null=True)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.products.productName