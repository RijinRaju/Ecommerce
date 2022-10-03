from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import context
from cart.models import CartItem
from .forms import OrderForm
from .models import Order,Payment,OrderProduct,SavedAddress
from shop.models import Products,Coupon
import datetime
from django.db.models import Max
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# Create your views here.

# authorize razorpay client with API Keys.
client = razorpay.Client(auth=(settings.KEY, settings.SECRET))



@login_required()
def payments(request,total=0,quantity=0):
    current_user = request.user
    print("order_id in COD",request.session.get('order_id'))
    order = Order.objects.get(user=current_user,is_ordered= False,id=request.session.get('order_id'))
    order_number = order.order_number


    cart_items=CartItem.objects.filter(user =current_user)
    for cart_item in cart_items:
        total += (cart_item.product.discount_price * cart_item.quantity)
        quantity += cart_item.quantity
    delivery_charge=40
    grand_total = delivery_charge + total


    # if coupon code is present...............
    if 'coupon_id' in request.session:
        coupon = Coupon.objects.get(id=request.session.get('coupon_id'))
        coupon_amount = coupon.maximum_discount_amount
        grand_total = grand_total - coupon_amount

    # checking is it cash on delivery
    if request.method =="POST":
        payment = request.POST['payment']
        if payment == "COD":
            pay= Payment()
            pay.user = current_user
            pay.amount_paid = grand_total
            pay.payment_method = payment
            pay.status = "success"
            pay.save()
            order.payment = pay
            order.is_ordered = True
            order.save()
            # creating an order id for cash on delivery
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            pay_id = current_date + str(pay.id)
            pay.payment_id=pay_id
            pay.save()
            ## moving the cart items into orderproduct table
            for item in cart_items:
                orderprduct = OrderProduct()
                orderprduct.order_id = request.session.get('order_id')
                orderprduct.payment = pay
                orderprduct.user_id = request.user.id
                orderprduct.product_id = item.product_id
                orderprduct.quantity = item.quantity
                orderprduct.product_price = item.product.discount_price
                orderprduct.ordered = True
                orderprduct.save()
                product = Products.objects.get(id = item.product_id)
                product.quantity -= item.quantity
                product.save()
            # deleting item in cart after order is placed
            CartItem.objects.filter(user = request.user).delete()
            return redirect(success)
        else:
            return redirect(payment)
    order = Order.objects.get(user=current_user, is_ordered=False,order_number=order_number)
    context = {
            'order':order,
            'cart_items':cart_items,
            'grand_total':grand_total,
            'tax':delivery_charge,
            'total':total
            }
    return render(request,'orders/payment.html',context)


def pay_pal(request,total=0,quantity=0):
    current_user = request.user
    body = json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    print("paypal ",body)
    cart_items = CartItem.objects.filter(user=current_user)
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    ## moving the cart items into orderproduct table
    orderprduct = OrderProduct()
    for item in cart_items:
        print("order id in paypal",request.session.get('order_id'))
        orderprduct.order_id = request.session.get('order_id')
        orderprduct.payment = payment
        orderprduct.user_id = request.user.id
        orderprduct.product_id = item.product_id
        orderprduct.quantity = item.quantity
        orderprduct.product_price = item.product.discount_price
        orderprduct.ordered = True
        orderprduct.save()
        product = Products.objects.get(id=item.product_id)
        product.quantity -= item.quantity
        product.save()
    CartItem.objects.filter(user=request.user).delete()
    data = {

        'transID':payment.payment_id,
        'orderID':orderprduct.id

    }
    print("paypal payment object",data)
    return JsonResponse(data)


def razor_pay(request):
    razor_data = json.loads(request.body)
    print("razor_data",razor_data['total']) 
    print("razor_status",razor_data['status'])
    print("inside razor pay...............")
    grand_total = razor_data['total'] 
    current_user = request.user
    # capture the payemt
    
    order = Order.objects.get(user=current_user,is_ordered= False,id=request.session.get('order_id'))
    cart_items = CartItem.objects.filter(user=current_user)
    order.order_number = razor_data['orderID']
    order.save()
    payment = Payment(
        user=request.user,
        payment_id=razor_data['orderID'],
        payment_method="RazorPay",
        amount_paid=razor_data['total'],
        status=razor_data['status'],

    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    for item in cart_items:
        orderprduct = OrderProduct()
        orderprduct.order_id = request.session.get('order_id')
        orderprduct.payment = payment
        orderprduct.user_id = request.user.id
        orderprduct.product_id = item.product_id
        orderprduct.quantity = item.quantity
        orderprduct.product_price = item.product.discount_price
        orderprduct.ordered = True
        orderprduct.save()
        product = Products.objects.get(id=item.product_id)
        product.quantity -= item.quantity
        product.save()
    print("cart item removed before")
    CartItem.objects.filter(user=request.user).delete() 
    print("cart item removed")   
    payment.save()
    return  redirect(success)
            




@login_required(login_url='login')
def add_address(request):
    current_user = request.user
    if request.method =="POST":
        form = OrderForm(request.POST)
        if form.is_valid():  # if the form valid it will store all the bill address data to database
            data = SavedAddress()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['zip_code']
            data.save()
            return redirect('checkout')
    return render(request,'orders/add_address.html')


@login_required(login_url='login')
def place_order(request,total=0,quantity=0):
    current_user = request.user
    dis_total = 0
    #checking if the cart is empty


    cart_items = CartItem.objects.filter(user =current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('home')

    grand_total = 0
    delivery_charge = 0

    for cart_item in cart_items:
        total += (cart_item.product.discount_price * cart_item.quantity)
        quantity += cart_item.quantity
        dis_total += cart_item.quantity * cart_item.dis_amt



    delivery_charge = 40
    grand_total = delivery_charge + total-dis_total
    
    # if coupon code is present...............
    if 'coupon_id' in request.session:
        coupon = Coupon.objects.get(id=request.session.get('coupon_id'))
        coupon_amount = coupon.maximum_discount_amount
        grand_total = grand_total - coupon_amount
    
    if 'coupon_id' in request.session:
        messages.info(request, coupon_amount)

    
    if request.user.is_authenticated and request.user.is_superadmin == False :
        if request.method == "GET":
            add_id = request.GET.get('s_adds')
            sav_addr = SavedAddress.objects.get(id=add_id)
            print("saved Address",sav_addr)
            data = Order()
            data.user = current_user
            data.first_name = sav_addr.first_name
            data.last_name = sav_addr.last_name
            data.phone = sav_addr.phone
            data.email= sav_addr.email
            data.address_line_1 = sav_addr.address_line_1
            data.address_line_2 = sav_addr.address_line_2
            data.country= sav_addr.country
            data.state = sav_addr.state
            data.city = sav_addr.city
            data.zip_code = sav_addr.pincode
            data.order_total = grand_total
            data.tax = delivery_charge
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generating the order id
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date =  d.strftime("%Y%m%d")
            order_number = current_date+str(data.id)
            
            data.save()
            request.session['order_id'] = data.id

            ### razor pay account details.............
            razor_payment = client.order.create({"amount": int(grand_total) * 100,"currency": "INR",})

            print("razor_order_detils",razor_payment)
            data.order_number = razor_payment['id']
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=razor_payment['id'])

            context = {
             'order': order,
             'cart_items': cart_items,
             'total': total,
             'delivery_charge': delivery_charge,
             'grand_total': grand_total,
             'razorpay_amount':razor_payment['amount'],
             'razorpay_status':razor_payment['status'],
                }
            return  render(request,'orders/payment.html',context)
           
    else:
        return redirect('login')



@csrf_exempt
def success(request):
    print("success page is here")
    current_user=request.user
    order = Order.objects.filter(user=current_user, is_ordered=False).last()
    # if 'razor_pay' in request.session:
        
    if order is not None:
        print("order_id",order.order_number)
        if 'coupon_id' in request.session:
            del request.session['coupon_id']
    context={
        'order':order
    }
    return render(request,'orders/success.html',context)