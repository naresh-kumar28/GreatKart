from django.db.models import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from carts.models import Cart, CartItem
from store.models import Product

# Create your views here.

# Yeh file carts related view functions rakhti hai. Neeche har function ke upar
# simple Hinglish (Hindi+English) comments diye gaye hain taaki code samajhna
# asaan ho — jaise session management, cart creation, item add karna, aur
# cart total calculate karna.

def _cart_id(request):
    # _cart_id: session se cart_id nikalta hai.
    # Agar session key exist nahi karti, to naya session create karke
    # uska key return karta hai. (Simple session-based cart id)
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # add_cart: product ko cart mein add karta hai.
    # Step 1: session ke cart_id se Cart fetch karo.
    try:
        # Agar cart pehle se exist karta hai to use lo
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        # Nahin to naya Cart create karo aur save karo
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    # Step 2: CartItem check karo — agar same product already hai to
    # uski quantity badhao, warna naya CartItem bana do.
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # Pehli baar product add ho raha hai
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        cart_item.save()

    # Kaam ho gaya — user ko cart page par redirect karo
    return redirect('cart')

def remove_cart(request, product_id):
    # remove_cart: cart se ek item ko remove karta hai.
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
   
    return redirect('cart')

def remove_cart_item(request, product_id):
    # remove_cart_item: cart se ek item ko completely remove karta hai.
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
   
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            # Har cart_item ke liye total aur quantity calculate karo
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (0.18 * total)  # 18% GST tax
        grand_total = total + tax
    except ObjectDoesNotExist:
        # Agar cart nahi mila (e.g. session expired ya empty cart),
        # to simply pass kar do — template mein zero values handle honge.
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total
    }
        
    return render(request, 'store/cart.html', context)