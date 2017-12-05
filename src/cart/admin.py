from django.contrib import admin
from .models import Cart
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subtotal']

    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)