from django.db import models
from django.db.models.signals import pre_save, post_save
from cart.models import Cart
import uuid
from mainwebsite.utils import unique_order_id_generator
# Create your models here.


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
    ('delivered', 'Delivered')
)


class Order(models.Model):
    order_id = models.CharField(max_length=225, editable=False)
    cart = models.ForeignKey(to=Cart)
    status = models.CharField(max_length=225, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.order_id

    def update_total(self):
        self.total = self.cart.subtotal + self.cart.shipping
        self.save()


def pre_save_connector_order_id(sender,instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_connector_order_id, sender=Order)


def post_save_connector_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.subtotal + cart_obj.shipping
        qs = Order.objects.filter(cart=cart_obj)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_connector_total, sender=Cart)


def post_save_connector_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_connector_order, sender=Order)