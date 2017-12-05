from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product
from categories.models import Category
from cart.models import Cart
# Create your views here.


class ProductListView(ListView):
    template_name = 'products/product_list.html'

    def get_queryset(self):
        qs = Product.objects.filter(description__icontains='macbook')[:50]
        return qs


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











