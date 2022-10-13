from django.shortcuts import render
from django.shortcuts import redirect
from .models import Customers
from twilio.rest import Client
import pyotp
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import auth
from cart.models import Cart,CartItem
from cart.views import _cart_id
import random
import string
from django.conf import settings
from shop.models import Referal_code
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        user_data = auth.authenticate(email=email, password=password,status="ACTIVE")
        if user_data:
            try:
                print("inside the try")
                cart = Cart.objects.get(cart_id = _cart_id(request))# checking is it any cart item is present
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    print("userdata:",user_data)
                    for item in cart_item:
                        item.user = user_data
                        item.save()
            except:
                pass
            auth.login(request, user_data)
            print("user:", request.user.is_authenticated)
            request.session['customer'] = email
            return redirect('/',user_data=user_data)
        elif Customers.objects.filter(status="BLOCK"):
            messages.info(request,"you are blocked ")
            return render(request, 'customers/login.html')
        else:
            messages.info(request,'invalid credentials')
    return render(request, 'customers/login.html')


def otp_auth(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        request.session['phone'] = phone

        if Customers.objects.filter(phone=phone).exists():
            # totp= pyotp.TOTP('base32secret3232').now()
            request.session['phone_no'] = phone

            client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            verification = client.verify \
                .services(settings.SERVICE) \
                .verifications \
                .create(to='+91'+phone, channel='sms')
            

            return redirect(verify_otp)
        else:

            messages.info(request, "invalid number")
            return render(request, 'customers/verify.html')
    else:
        return render(request, 'customers/verify.html')




def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        phone_no = request.session['phone_no']
        print(phone_no)
        if Customers.objects.filter(phone=phone_no).exists():
            user = Customers.objects.get(phone=phone_no)

            client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            verification_check = client.verify \
                .services(settings.SERVICE) \
                .verification_checks \
                .create(to='+91'+phone_no, code=otp)
            if verification_check.status == "approved":
                auth.login(request,user)
                request.session['customer'] = request.session.get('phone')
                return redirect('/')
            else:
                messages.info(request,'invalid OTP')
                return render(request, 'customers/verify_auth.html')
        else:
            messages.info(request, 'invalid phone number')
            return render(request, 'customers/verify_auth.html')
    else:
        return render(request, 'customers/verify_auth.html')

@never_cache
def logout(request):
    auth.logout(request)
    return redirect('/')




def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        if Customers.objects.filter(username=username).exists():
            messages.info(request,'username is already exists')
            return redirect('signup')
        elif Customers.objects.filter(email=email).exists():
            messages.info(request,'email is already taken')
            return redirect('signup')
        elif Customers.objects.filter(phone=phone).exists():
            messages.info(request,'Mobile number is already taken')
            return redirect('signup')

        else:
            add_customer = Customers.objects.create_user(name=name,username=username,address=address,email=email,phone=phone,password=password)
            add_customer.save()
            refer = Referal_code()
            size = 6
            referal_code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=size))
            refer.referal_code = referal_code
            refer.user = add_customer
            refer.save()
            
            return redirect(login)
    return render(request, 'customers/signup.html')

