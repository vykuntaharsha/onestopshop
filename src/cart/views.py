from django.shortcuts import render

# Create your views here.


def cart_home(request):
    return render(request, 'cart/cart_home.html', {})
