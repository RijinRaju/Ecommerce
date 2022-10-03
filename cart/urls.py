from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<str:product_id>/<int:cart_item_id>/',views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name ='checkout'),
    path('cart_prod_inr/',views.cart_prod_inr,name='cart_prod_inr'),
    path('cart_prod_dec/',views.cart_prd_dec,name='cart_prod_dec'),
    path('coupon_code/',views.coupon_code,name="coupon_code"),

]