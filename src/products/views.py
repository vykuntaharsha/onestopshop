from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product
from.utils import unique_slug_generator
from django.http import Http404
# Create your views here.


class ProductListView(ListView):
    template_name = 'products/product_list.html'

    def get_queryset(self):
        qs = Product.objects.all()[:10]
        return qs


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        slug = kwargs.get('slug')
        print(slug)
        instance = self.queryset.filter(slug=slug)
        context[object] = instance
        return context











