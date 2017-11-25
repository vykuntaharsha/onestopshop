from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm


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


def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {
        'form': login_form
    }
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context['form'] = login_form
            return redirect('/')
        else:
            print('error')
    return render(request, template_name='auth/login.html', context=context)


User = get_user_model()


def register_page(request):
    register_form = RegisterForm()
    context = {
        'form': register_form
    }
    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        new_user = User.objects.create_user(username,email,password)
        redirect('/login')
    return render(request, template_name='auth/register.html', context=context)
