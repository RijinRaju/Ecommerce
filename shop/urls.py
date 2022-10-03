from django.urls import path
from .views import home,detailed_view,search_view,shop_view,order_view
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('detailed_view/<int:id>',detailed_view, name='detailed_view'),
    path('shop_view/',shop_view,name='shop_view'),
    path('search_view/',search_view, name='search_view'),
    path('filter/<int:price>/',views.filter,name="filter"),
    path('order_view/',order_view, name='order_view'),
    path('order_detailed_view/<int:id>',views.order_detailed_view,name='order_detailed_view'),
    path('cancel_orders_view/<int:id>', views.cancel_orders_view,name='cancel_orders_view'),


    path('category_view/<int:id>',views.category_view,name='category_view'),
    path('invoice_gen/<int:id>', views.invoice_gen, name='invoice_gen'),

    path('profile/',views.profile,name='profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('return_product/<int:id>',views.return_product,name="return_product"),
    path('wallet/',views.wallet,name="wallet"),

    path('review/<int:product_id>',views.review,name="review"),
]