from django.urls import path
from . import views
urlpatterns = [

    path('admin_login/',views.login,  name='admin_login'),
    path('home/',views.home, name='admin_home'),
    path('admin_logout/',views.admin_logout, name='admin_logout'),

    path('products/',views.products, name='products'),
    path('add_product/',views.add_product, name='add_product'),
    path('products/edit_product/<int:id>',views.edit_product, name='edit_product'),
    path('products/delete_product/<int:id>',views.delete_product, name='delete_product'),

    path('users/',views.users, name='users'),
    path('users/block_user/<int:id>',views.block_user, name='block'),

    path('orders/',views.orders, name='orders'),
    path('orders/order_details/<int:id>',views.order_details,name='order_details'),

    path('category/',views.CategoryList.as_view(), name='category'),
    path('category_create/',views.add_category, name='category_create'),
    path('category_update/<slug:pk>',views.CategoryUpdate.as_view(), name='category_update'),
    path('category_delete/<slug:pk>',views.Category_delete.as_view(), name='category_delete'),

    path('sub_category/', views.subCategoryList, name='sub_category'),
    path('sub_category_create/', views.SubCategoryCreate.as_view(), name='sub_category_create'),
    path('sub_category_update/<slug:pk>', views.SubCategoryUpdate.as_view(), name='sub_category_update'),
    path('sub_category_delete/<slug:pk>',views.Subcategory_delete.as_view(), name='sub_category_delete'),

    path('coupons/',views.coupons,name='coupons'),
    path('add_coupon/',views.add_coupon,name="add_coupon"),
    path('edit_coupon/<int:id>/',views.edit_coupon,name="edit_coupon"),
    path('delete_coupon/<int:id>/',views.delete_coupon,name="delete_coupon"),
   
    path('add_category_offer/',views.add_category_offer,name="add_category_offer"),
    path('delete_category_offer/<int:id>/',views.delete_category_offer,name="delete_category_offer"),
    path('edit_category_offer/<int:id>/',views.edit_category_offer,name="edit_category_offer"),

    path('add_product_offer/', views.add_product_offer, name="add_product_offer"),
    path('edit_product_offer/<int:id>/', views.edit_product_offer, name="edit_product_offer"),
    path('delete_product_offer/<int:id>/', views.delete_product_offer, name="delete_product_offer"),

    path('banners/',views.banner,name='banner'),
    path('add_banners/',views.add_banner,name='add_banners'),
    path('banners/update_banners/<int:id>', views.update_banner, name='update_banners'),
    path('banners/delete_banners/<int:id>', views.delete_banner, name='delete_banners'),


    path('sales/',views.sales,name="sales"),
    path('monthly_sales/',views.monthly_sales,name="month_sales"),
    path('yearly_sales/',views.yearly_sales,name="year_sales"),
    path('export_to_excel/',views.export_to_excel,name="export_to_excel"),
    path('export_to_pdf/',views.export_to_pdf,name="export_to_pdf"),
    path('export_to_csv/',views.export_to_csv,name="export_to_csv"),
]