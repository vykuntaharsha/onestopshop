from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product
# Create your views here.


class ProductListView(ListView):
    template_name = 'products/product_list.html'

    def get_queryset(self):
        qs = Product.objects.filter(description__icontains='macbook')[:50]
        return qs


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        slug = kwargs.get('slug')
        instance = self.queryset.filter(slug=slug)
        context[object] = instance
        return context











