from django.shortcuts import render,redirect
from django.template import context
from .models import Category_offer, Products, Banners,Category,Referal_code,Wallet,Coupon,Product_offer,Rating
from django.core.paginator import Paginator
from datetime import datetime,timedelta
from customers.models import Customers
from customers.views import login, logout
from orders.models import  OrderProduct
from django.db.models import Q
from orders.models import SavedAddress
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
import sweetify
from django.contrib.auth.models import auth
import json
import random
import string


def home(request):
    products = Products.objects.all()
    banners = Banners.objects.all()
    category= Category.objects.all()
    category_offer = Category_offer.objects.all()
    product_offer = Product_offer.objects.all()

   
    if 'customer' in request.session:
        cus_si = request.session.get('customer')
        print("in home",cus_si)
        user = Customers.objects.filter(Q(email =request.user) | Q(phone = request.session.get('customer')) )
        print("users are",user)
        p = Paginator(products, 9)
        page = request.GET.get('page')
        prod = p.get_page(page)

        

        context = {
            'prod_page':prod,
            'user':user,
            'banners':banners,
            'category':category,
            'category_offer':category_offer,
            'product_offer':product_offer
        }
        return render(request, 'shop/home.html',context)
    else:
        p=Paginator(products,4)
        page=request.GET.get('page')
        prod=p.get_page(page)
        context={
            'prod_page':prod,
            'banners':banners,
            'category':category,
        }
        return render(request,'shop/home.html',context)

    return render(request, 'shop/home.html',{'prod_page':prod,'banners':banners})


def detailed_view(request,id):
    product = Products.objects.get(id=id)
    category_offer = Category_offer.objects.all()
    all_products = Products.objects.all()
    review  = Rating.objects.filter(product = id)
    if 'customer' in request.session:
        if request.method == 'POST':
            quantity = request.POST['quantity']
            request.session['productQuantity'] = quantity
            print("quantity:",request.session.get('productQuantity'))
        user_session = request.session.get('customer')
        user=Customers.objects.get(email=user_session)

        context = {
            'product_view':product,
            'user':user,
            'all_products':all_products,
            'category_offer':category_offer,
            'review':review
        }        
        return render(request, "shop/detail.html",context)

    return render(request, 'shop/detail.html', {'product_view': product, 'all_products': all_products})


def shop_view(request):
    prices = [30000,50000,70000,90000,100000]
    products=Products.objects.all()
    category_offer = Category_offer.objects.all()
    product_offer = Product_offer.objects.all()
    p=Paginator(products,9)
    page = request.GET.get('page')
    prod = p.get_page(page)
    if request.method == "POST":
        search_name=request.POST["search_name"]
    context ={
        'prod_page': prod,
        'prices': prices,
        'category_offer':category_offer,
        'product_offer':product_offer

    }
    return render(request,'shop/shop.html',context)



def search_view(request):
    prices = [30000, 50000, 70000, 90000, 100000]
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Products.objects.order_by('-create_date').filter(productName__icontains=keyword)
            context = {
                'product':products,
                'prices':prices,
            }
            return render(request,'shop/search.html',context)
        return redirect('home')
    else:
        return render(request, 'shop/search.html')


def order_view(request):
    user = request.user
    print("user_ud in shop:",user.id)
    orders = OrderProduct.objects.filter(user= user.id)
    p = Paginator(orders,3)
    page = request.GET.get('page')
    prod = p.get_page(page)

    return render(request,'shop/order.html',{"orders":prod})


def order_detailed_view(request,id):
    order_prod = OrderProduct.objects.get(id =id)
    current_date = datetime.now()
    print("current date",current_date)
    print("3 days later",order_prod.exp_date)
    return render(request,'shop/home_order_details.html',{'order_data':order_prod,'current_date':current_date})


def return_product(request,id):
    order_product = OrderProduct.objects.get(id=id)
    dt = datetime.now()
    ts = timedelta(days=3)
    exp_date = dt + ts

    if order_product.product_return == False:
        order_product.product_return = True
        order_product.exp_date = exp_date 
        order_product.save()
        print("expiary date",order_product.exp_date)
        sweetify.success(request, 'Your product will be Returned')
    else:
        sweetify.warning(request, 'Return is always placed')
        
    return redirect('order_detailed_view',id)




def invoice_gen(request,id):
    order_data = OrderProduct.objects.filter(id=id)
    template_path = 'shop/invoice.html'
    context = {'order_data': order_data}

    response = HttpResponse(content_type='application/pdf') #csv file can also be generated using content_type='application/csv
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response






def cancel_orders_view(request,id):
    order = OrderProduct.objects.get(id = id)
    order.ordered = False
    order.save()
    return redirect('order_view')

def category_view(request,id):
    products = Products.objects.filter(category = id)
    prices = [30000,50000,70000,90000,100000]
    return render(request,'shop/search.html',{'product':products,'prices':prices})

def filter(request,price):
    prices = [30000,50000,70000,90000,100000]
    products = Products.objects.order_by('-create_date').filter(discount_price__lt=price)
    context = {
        'product': products,
        'prices': prices,
    }
    return render(request, 'shop/search.html',context)

def profile(request):

    coin = 0
    wallet = Wallet.objects.filter(user= request.user)
    for sum in wallet:
        coin += sum.coin
    
    try:
        referal_code =Referal_code.objects.get(user=request.user)
    except:
        refer_code = Referal_code()
        size = 6
        referal_code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=size))
        refer_code.referal_code = referal_code
        refer_code.user = request.user
        refer_code.save()

    user = Customers.objects.get(email=request.user)
    address = SavedAddress.objects.filter(user=user.id)
    orders = OrderProduct.objects.filter(user=user.id)
    if request.method == 'POST':

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            customers = Customers.objects.get(id=request.user.id)
            customers.set_password(password)
            customers.save()
            sweetify.success(request, "password updated successfully")
            auth.logout(request)
            return redirect('login')
        else:
            sweetify.error(request,"Password doesnt Match")
            return redirect('profile')
    if referal_code != None:
        ref_code = referal_code
    context ={
        'user':user,
        'address':address,
        'orders': orders,
        'referal_code':ref_code,
        'coins':coin
    }
    return render(request,'shop/profile.html',context)



def edit_profile(request):
    user = Customers.objects.get(email=request.user)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.username  = request.POST.get('user_name')
        user.address = request.POST.get('address')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.save()
        sweetify.success(request, 'Your changes are Saved')
    return redirect(profile)


def wallet(request):
    current_user = request.user
    
    if request.method == "POST":
        code = request.POST['referal_code']
        print("code:",code)
        if code :
            
            try:
                refer = Referal_code.objects.get(referal_code=code)
                wallet = Wallet()
                wallet.user = refer.user
                wallet.coin = 50
                wallet.save()

                wallet = Wallet()
                user_refer_code = Referal_code.objects.get(user=request.user)
                wallet.user = user_refer_code.user
                wallet.coin = 20
                wallet.save()
                sweetify.success(request, "20 coins added to your wallet")
            except:
                sweetify.warning(request,"invalid Referar code")
    return redirect(profile)



def review(request,product_id):
    if request.user:
        rate = Rating()
        if request.method == 'POST':
            rate.rate = request.POST['rate']
            rate.post = request.POST['message']
            rate.user = request.user
            rate.email = request.POST['email']
            prod = Products.objects.get(id = product_id)
            rate.product = prod
        rate.save()
    else:
        return redirect(login)
    return redirect(detailed_view, product_id)