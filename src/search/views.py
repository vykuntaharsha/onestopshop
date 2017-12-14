from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
# Create your views here.


class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Product.objects.search(query=query)[:50]
        return Product.objects.all()[:50]
