from django.db import models
from django.forms import DateTimeField
from customers.models import Customers
from shop.models import Products
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Customers,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out of delivery','Out of delivery'),
         ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
       
    )

    user = models.ForeignKey(Customers, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField(null=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='Confirmed')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name}{self.last_name}'

    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2},{self.country}, {self.state},{self.city},{self.zip_code}'

    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_return = models.BooleanField(default=False,null=False)
    exp_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.productName





class SavedAddress(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100)
    city =  models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField(null=True)
    user = models.ForeignKey(Customers,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.name
    
    