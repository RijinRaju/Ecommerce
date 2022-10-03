from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city','zip_code']


class statusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)