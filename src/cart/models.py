from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed
# Create your models here.


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                user_cart = self.model.objects.filter(user=request.user).first()
                if user_cart is not None:
                    cart_obj.products.add(*user_cart.products.all())
                    cart_obj.user = request.user
                    cart_obj.save()
                    user_cart.delete()
                else:
                    cart_obj.user = request.user
                    cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                cart_obj = self.model.objects.filter(user=user).first()
                if cart_obj is not None:
                    return cart_obj
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):

    user = models.ForeignKey(to=User, null=True, blank=True)
    products = models.ManyToManyField(to=Product, blank=True)
    subtotal = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    shipping = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_save_cart_connector(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        shipping = 0
        for x in products:
            total += x.price
            shipping += x.shipping
        instance.subtotal = total
        instance.shipping = shipping
        instance.save()


m2m_changed.connect(m2m_save_cart_connector, sender=Cart.products.through)
