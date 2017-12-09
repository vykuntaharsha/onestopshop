from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product
from cart.models import Cart
import random
# Create your views here.


class ProductListView(ListView):
    template_name = 'products/product_list.html'

    def get_queryset(self):
        start_ = random.randint(0, 30000)
        qs = Product.objects.all()[start_:start_+50]
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        self.request.session['cart_products'] = cart_obj.products.count()
        context['cart'] = cart_obj

        return context


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    queryset = Product.objects.all()

    def get_context_data(self, * args, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        slug = kwargs.get('slug')
        instance = self.queryset.filter(slug=slug)
        context[object] = instance
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context











