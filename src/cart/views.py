from django.shortcuts import render, redirect, HttpResponse
from .models import Cart
from products.models import Product
# Create your views here.


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if request.user.is_authenticated:
        request.session['cart_products'] = Cart.objects.filter(user=request.user).first().products.count()
    return render(request, 'cart/cart_home.html', {'cart': cart_obj})


def cart_update(request):

    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get_by_id(_id=product_id).first()
        except Product.DoesNotExist:
            print('product is out of stock')
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_products'] = cart_obj.products.count()

        return redirect('cart:home')