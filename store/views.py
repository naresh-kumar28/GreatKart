from django.shortcuts import get_object_or_404, render

from carts.models import CartItem
from carts.views import _cart_id
from .models import Product
from category.models import Category

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    context = {
        'products' : products,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    
    context = {
        'product': product,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)
