from django.shortcuts import render,redirect
from shop.models import Products
from .models import  Wishlist,WishlistItem
# Create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


def add_wishlist(request,id):
    product = Products.objects.get(id=id)
    try:
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))

    except Wishlist.DoesNotExist:

        wishlist = Wishlist.objects.create(
            wishlist_id = _wishlist_id(request)
        )

    if request.user.is_authenticated:
        try:
            wishlist_item = WishlistItem.objects.get(products = product,user = request.user)
            wishlist_item.save()
        except WishlistItem.DoesNotExist:
            wishlist_item = WishlistItem.objects.create(
                products = product,
                user=request.user
            )
            wishlist_item.save()

    return redirect('wishlist')


def wishlist(request):
    if request.user.is_authenticated:
        wishlistitem = WishlistItem.objects.filter(user = request.user)

        context = {
            'wishlistitem':wishlistitem
        }
        return render(request,'wishlist/wishlist.html',context)
    else:
        return render(request,'wishlist/wishlist.html')


def remove_wishlist(request,id):
    product = Products.objects.get(id=id)
    wishlist = WishlistItem.objects.filter(products = product,user=request.user)
    wishlist.delete()
    return redirect('wishlist')
