from django.urls import path
from . import views
urlpatterns = [

    path('place_order/',views.place_order,name="place_order"),
    path('payments/',views.payments,name="payments"),
    path('pay_pal/',views.pay_pal,name="pay_pal"),
    path('razor_pay/',views.razor_pay,name="razor_pay"),
    path('success/',views.success,name="success"),
    path('add_address/',views.add_address,name="add_address"),
]