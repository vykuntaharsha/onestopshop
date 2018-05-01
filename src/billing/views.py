from django.shortcuts import render, HttpResponse, redirect
from django.utils.http import is_safe_url
import stripe
from django.http import JsonResponse
from .models import BillingProfile, Card
from django.conf import settings
# Create your views here.


STRIPE_API_KEY = getattr(settings, 'STRIPE_API_KEY', '')
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', '')

stripe.api_key = STRIPE_API_KEY



def payment_method_view(request):
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('cart:home')

    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_create_view(request):

    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({'message': 'cannot find this user'}, status_code=404)
        token = request.POST.get('token')
        if token is not None:
            new_card = Card.objects.add_new(billing_profile,token)
        return JsonResponse({'message': 'Success! Your card is added.'})
    raise HttpResponse("error", status_code=401)
