from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressCheckoutForm
from addresses.models import Address
from django.http import JsonResponse
from django.conf import settings
import stripe
# Create your views here.

STRIPE_API_KEY = getattr(settings, 'STRIPE_API_KEY', 'sk_test_kEepAt1GDvVRsnwHZkKQNs1a')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', 'pk_test_vkJRqUc0sr2Xsg0v12iMKtup')

stripe.api_key = STRIPE_API_KEY


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        'name': product.name,
        'price': product.price,
        'image': product.image_url,
        'url': product.get_absolute_url(),
        'id': product.id
    } for product in cart_obj.products.all()]
    cart_json = {'products': products, 'subtotal': cart_obj.subtotal, 'shipping': cart_obj.shipping}
    return JsonResponse(cart_json)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if request.user.is_authenticated():
        request.session['cart_products'] = cart_obj.products.count()
    return render(request, 'cart/cart_home.html', {'cart': cart_obj})


def cart_update(request):

    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get_by_id(_id=product_id).first()
        except Product.DoesNotExist:
            print('product is out of stock')
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_products'] = cart_obj.products.count()

        if request.is_ajax():
            json_data = {
                'added': added,
                'removed': not added,
                'cartProductsCount': cart_obj.products.count()
            }
            return JsonResponse(json_data)
        return redirect('cart:home')


def checkout_home(request):

    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressCheckoutForm()
    address_qs = None
    has_card = False

    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == 'POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, charge_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                cart_obj.active = False
                cart_obj.save()
                request.session['cart_products'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect('cart:success')
            else:
                return redirect('cart:checkout')

    context = {
        'order': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
        'has_card': has_card,
        'publish_key': STRIPE_PUB_KEY,
    }
    return render(request,'cart/checkout.html', context)


def checkout_done_view(request):
    return render(request, template_name='cart/checkout-done.html', context={})
