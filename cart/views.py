
from django.shortcuts import render,redirect,get_object_or_404
from customers.models import Customers
from owner.views import login
from shop.models import Category_offer, Product_offer, Products,Coupon
from .models import CartItem,Cart
from orders.models import Order,SavedAddress
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import sweetify
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    product= Products.objects.get(id=product_id)
    product_offer_amount = 0
    category_offer_amount = 0
    category_offer = Category_offer.objects.all()

    if request.user.is_authenticated:
        try:
            cart= Cart.objects.get(cart_id =_cart_id(request))
        except:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()
        try:
            cart_item = CartItem.objects.get(product=product,cart=cart,user=request.user)
            cart_item.quantity += 1  # pressing first time cart button
            cart_item.save()
            # new code for offer ..............
            try:
                print("hello try")
                product_offer = Product_offer.objects.get(product=cart_item.product)
                if product_offer:
                    print("offer........... ",product_offer)
                    product_offer_amount += product_offer.offer_amount
                    print("product offer amount", product_offer_amount)
                    for cat_off in category_offer:
                        if cart_item.product.category == cat_off.category:
                            prod = Products.objects.filter(category=cat_off.category)
                            amt1 = int(cat_off.offer_percent)/100
                            print("amt1", amt1)
                            for pro in prod:
                                if product_offer.product == pro:
                                    amt2 = amt1 * pro.discount_price
                                    category_offer_amount += amt2
                                    print("category_offer_amount",category_offer_amount)
                    if product_offer_amount > category_offer_amount:
                        cart_item.dis_amt = product_offer_amount
                        cart_item.save()
                    else:
                        cart_item.dis_amt = category_offer_amount
                        cart_item.save()
                
            except:
                pass
        # end here.................
           
            print("cart_quantity:",cart_item.quantity)

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
                cart=cart,
            )
            cart_item.save()
            # new code for offer ..............
            
            print("except block")
               
            try:
                product_offer = Product_offer.objects.get(
                    product=cart_item.product.id)
                print("product", product_offer)
                product_offer_amount += product_offer.offer_amount
                print("product offer amount", product_offer_amount)
                for cat_off in category_offer:
                    if cart_item.product.category == cat_off.category:
                        prod = Products.objects.filter(category=cat_off.category)
                        amt1 = int(cat_off.offer_percent)/100
                        print("amt1", amt1)
                        for pro in prod:
                            if product_offer.product == pro:
                                amt2 = amt1 * pro.discount_price
                                category_offer_amount += amt2
                                print("category_offer_amount",
                                    category_offer_amount)
                if product_offer_amount > category_offer_amount:
                    cart_item.dis_amt = product_offer_amount
                    cart_item.save()
                else:
                    cart_item.dis_amt = category_offer_amount
                    cart_item.save()
            except:


                print("except condition")
                for cat_off in category_offer:
                    if cart_item.product.category == cat_off.category:
                        prod = Products.objects.filter(
                            category=cat_off.category)
                        amt1 = int(cat_off.offer_percent)/100
                        print("amt1", amt1,cat_off.offer_percent)
                        for pro in prod:
                            if pro.id == cart_item.product.id:
                                amt2 = amt1 * pro.discount_price
                                category_offer_amount += amt2
                                print("category_offer_amount",
                                        category_offer_amount)
                                
                                cart_item.dis_amt = category_offer_amount
                                cart_item.save()
                                print("cart_item discount amt", cart_item.dis_amt)
        # end here.................

    else:
        try:
            cart= Cart.objects.get(cart_id =_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1 #pressing first time cart button
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product =product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save()
    return  redirect('cart')


# increment view for Ajax call
def cart_prod_inr(request):
    body = json.loads(request.body)
    print("body data",body['quantity'],body['id'])
    product = Products.objects.get(id=body['id'])
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, user=request.user)
            cart_item.quantity +=1  # pressing first time cart button
            cart_item.total = body['total']
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
                cart=cart,
                total=body['total'],
            )
            cart_item.save()

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity +=1  # pressing first time cart button
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            cart_item.save()
    return redirect('cart')


def remove_cart(request,product_id,cart_item_id):
    product = get_object_or_404(Products,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


# decrement view for Ajax call
def cart_prd_dec(request):
    body = json.loads(request.body)
    product = get_object_or_404(Products, id=body['product_id'])
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=body['cartItem_id'])
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.total = body['total']
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request,product_id,cart_item_id):

    print("produc_id:",product_id,"cart_item_id",cart_item_id)

    product = get_object_or_404(Products, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item =  CartItem.objects.get(product =product,cart=cart )
    cart_item.delete()
    return redirect('cart')



def coupon_code(request):
    if request.user.is_authenticated:
        if request.method == "POST":
                coupon_code = request.POST['coupon_code']
                try:
                    coupons = Coupon.objects.get(coupon_code=coupon_code)
                    print("coupon", coupons)
                    if  coupons.is_Active == True:
                        
                        if coupons.user != request.user:
                            request.session['coupon_id'] = coupons.id
                            coupons.max_limit = coupons.max_limit - 1
                            coupons.user = request.user
                            coupons.save()
                            sweetify.success(request, "coupon is applied")
                        else:
                             sweetify.error(request, "Not Eligible for coupon")
                    else:
                        sweetify.error(request, "coupon is Expired")
                except:
                    sweetify.error(request, "coupon is Invalid")
        return redirect(cart)
    else:
        return redirect(login)




def cart(request,total=0,quantity=0,cart_items=None):
    delivery_charge = 0
    grand_total = 0
    total1=0

    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_Active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_Active=True)
        for cart_item in cart_items:
            total += (cart_item.product.discount_price * cart_item.quantity)
            print("total",total)

            quantity += cart_item.quantity

        for cart_item in cart_items:
            total1 += cart_item.quantity * cart_item.dis_amt

        if total > 1:
            delivery_charge = 40
            grand_total = delivery_charge +total - total1
        else:
            delivery_charge = 0
            grand_total = total
        if 'coupon_id' in request.session:
            messages.success(request,"coupon is applied in your purchase")
            
    except ObjectDoesNotExist:
        pass  # just ignore
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'delivery_charge':delivery_charge,
        'grand_total':grand_total

    }
    return render(request,'cart/cart.html',context)


@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    if request.user.is_authenticated:
        dis_total = 0
        try:
            delivery_charge = 0
            grand_total = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user,is_Active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_Active=True)

            for cart_item in cart_items:
                
                total += (cart_item.product.discount_price * cart_item.quantity)
                quantity += cart_item.quantity
            
            for cart_item in cart_items:
                dis_total += cart_item.quantity * cart_item.dis_amt

            delivery_charge = 40
            grand_total = delivery_charge + total - dis_total

            # if coupon code is present...............
            if 'coupon_id' in request.session:
                coupon = Coupon.objects.get(id=request.session.get('coupon_id'))
                coupon_amount = coupon.maximum_discount_amount
            
                grand_total = grand_total - coupon_amount

            if 'coupon_id' in request.session:
                messages.info(request, coupon_amount)

        except ObjectDoesNotExist:
            pass  # just ignore
        address = SavedAddress.objects.filter(user=request.user.id)

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'delivery_charge': delivery_charge,
            'grand_total': grand_total,
            'address': address,
            

        }
        return render(request, 'cart/checkout.html', context)
    else:
        return redirect('login')