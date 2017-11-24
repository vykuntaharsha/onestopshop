from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm


def home_page(request):
    context = {
        'title': 'Home',
        'content': 'welcome!'
    }
    return render(request, template_name='base.html', context=context)


def about_page(request):
    context = {
        'title': 'About',
        'content': 'we are awesome!'
    }
    return render(request, template_name='base.html', context=context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'contact',
        'content': 'Fill in the form to contact us!',
        'form': contact_form
    }
    return render(request, template_name='contact/view.html',context=context)

