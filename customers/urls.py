from django.urls import path
from .views import login, signup, otp_auth,verify_otp,logout

urlpatterns = [

    path('user_login/', login, name='login'),
    path('user_signup/', signup, name='signup'),
    path('otp_auth/', otp_auth, name='otp_auth'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('user_logout/', logout, name='user_logout'),

]