
from django.db import models
from django.urls import reverse
from customers.models import Customers
# Create your models here.


class Category(models.Model):
    title=models.CharField(max_length=100,null=True)
    url_slug=models.CharField(max_length=200,null=True)
    thumbnail=models.FileField(upload_to='static',default=0)
    description=models.TextField(max_length=250)
    category_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("category")

    def __str__(self):
        return self.title


class Sub_category(models.Model):
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description = models.TextField(max_length=250,null=True)

    def get_absolute_url(self):
        return reverse("sub_category")

    def __str__(self):
        return self.title



class Products(models.Model):
    productName= models.CharField(max_length=200)
    price=models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    quantity=models.IntegerField()
    descriptions=models.CharField(max_length=500)
    thumbnail=models.CharField(max_length=200)
    image1=models.ImageField(upload_to='static',null=True,blank=True)
    image2=models.ImageField(upload_to='static',blank=True)
    image3=models.ImageField(upload_to='static',blank=True)
    is_available = models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    create_date=models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.productName

class Product_category(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)


class Banners(models.Model):
    banner = models.ImageField(upload_to='static/banners',height_field=None,width_field=None,max_length=None,blank=True)
    title = models.CharField(max_length=100,null=True)
    name= models.CharField(max_length=50,null=True)
    is_select = models.BooleanField(default=False)


class Coupon(models.Model):
    title = models.CharField(max_length=100,null=False)
    date_created = models.DateField(auto_now=True)
    valid_until = models.DateTimeField(auto_now=False)
    coupon_code = models.CharField(max_length=20,null=False)
    maximum_discount_amount = models.IntegerField(null=False)
    is_redeem = models.BooleanField(default=False)
    is_Active = models.BooleanField(default=True)
    max_limit  = models.IntegerField(default=0,null=False)
    user = models.ForeignKey(Customers,on_delete=models.CASCADE,null=True)


class Category_offer(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=100,null=False)
    date_created = models.DateField(auto_now=True)
    valid_until = models.DateField(auto_now=False)
    offer_amount= models.IntegerField(default=0,null=False)
    is_Active = models.BooleanField(default=True)
    offer_percent = models.IntegerField(default=0,null=False)
      
class Product_offer(models.Model):
    offer_percent =models.IntegerField(default=0,null=False)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    offer_amount = models.IntegerField(default=0,null=False) 

class Referal_code(models.Model):
    referal_code = models.CharField(null=False,max_length=50)
    user = models.ForeignKey(Customers,on_delete=models.CASCADE)

class Wallet(models.Model):
    coin = models.IntegerField(default=0,null=False)
    user = models.ForeignKey(Customers,on_delete=models.CASCADE)


class Rating(models.Model):
    user = models.ForeignKey(Customers,on_delete = models.CASCADE)
    rate = models.IntegerField(default=0,null=False)
    post = models.TextField(null=False)
    email = models.EmailField(max_length=250,null=False)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    date = models.DateField(auto_now=True)