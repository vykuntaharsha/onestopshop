from django.shortcuts import render
from .forms import ContactForm
from cart.models import Cart
from django.http import JsonResponse, HttpResponse


def home_page(request):
    context = {
        'title': 'Home',
        'content': 'welcome!'
    }

    if request.user.is_authenticated:
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        request.session['cart_products'] = cart_obj.products.count()
    return render(request, template_name='home_page.html', context=context)


def about_page(request):
    context = {
        'title': 'About',
        'content': 'we are awesome!'
    }
    return render(request, template_name='home_page.html', context=context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'contact',
        'content': 'Fill in the form to contact us!',
        'form': contact_form
    }
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({'message': 'Thank you'})
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, template_name='contact/view.html', context=context)
