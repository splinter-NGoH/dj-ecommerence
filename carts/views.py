from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import PROTECT
from carts.models import Cart, Cart_Item
from store.models import Products, Variation
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
# Create your views here.
def _cart_id (request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product ,variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try: 
        cart_item = Cart_Item.objects.create(product = product, quantity = 1, cart = cart)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation: 
                cart_item.variations.add(item)

        # cart_item.quantity += 1
        cart_item.save()
    except Cart_Item.DoesNotExist:
        cart_item = Cart_Item.objects.create(product=product,quantity=1, cart=cart)
        if len(product_variation) > 0:
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()

        
    return redirect('cart')


def remove_cart (request, product_id, cart_item_id):
    product = get_object_or_404(Products, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cart_Item.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cart_Item.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
        
    return redirect('cart')


def remove_cart_item (request, product_id, cart_item_id):
    
    product = get_object_or_404(Products, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cart_Item.objects.get(user=request.user, product=product, id=cart_item_id)
            cart_item.delete()
        else:           
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cart_Item.objects.get(cart=cart, product=product, id=cart_item_id)
            cart_item.delete()

    except:
        pass  
    return redirect('cart')

def cart (request, total=0, quantity=0, cart=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cart_Item.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cart_Item.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2 * total)/100 
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items':cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html',context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart=0, cart_items=None):
    tax =0
    grand_total=0
    try:
        if request.user.is_authenticated:
            cart_items = Cart_Item.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cart_Item.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2 * total)/100 
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items':cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)