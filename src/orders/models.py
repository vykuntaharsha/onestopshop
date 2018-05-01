from django.db import models
from django.db.models.signals import pre_save, post_save
from cart.models import Cart
from billing.models import BillingProfile
from mainwebsite.utils import unique_order_id_generator
from addresses.models import Address
from django.core.urlresolvers import reverse
# Create your models here.


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
    ('delivered', 'Delivered')
)


class OrderManagerQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
                billing_profile=billing_profile,
                cart=cart_obj,
                active=True,
                status='created'
            )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile,
                    cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(to=BillingProfile)
    order_id = models.CharField(max_length=225, editable=False)
    shipping_address = models.ForeignKey(to=Address, null=True, related_name='shipping_address')
    billing_address = models.ForeignKey(to=Address, null=True, related_name='billing_address')
    shipping_address_final = models.TextField(blank=True, null=True)
    billing_address_final = models.TextField(blank=True, null=True)
    cart = models.ForeignKey(to=Cart)
    status = models.CharField(max_length=225, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp', '-updated']

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id': self.order_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping Soon"

    def update_total(self):
        self.total = self.cart.subtotal + self.cart.shipping
        self.save()

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if shipping_address and billing_profile and billing_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_connector_order_id(sender,instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.delete()
    if instance.shipping_address and not instance.shipping_address_final:
        instance.shipping_address_final = instance.shipping_address.get_address()

    if instance.billing_address and not instance.billing_address_final:
        instance.billing_address_final = instance.billing_address.get_address()


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