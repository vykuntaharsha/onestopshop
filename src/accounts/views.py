from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login, get_user_model, logout
from .models import GuestEmail

# Create your views here.

User = get_user_model()


def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {
        'form': login_form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(to=redirect_path)
            else:
                context['form'] = login_form
                return redirect('home')
        else:
            print('error-login_page')
    return render(request, template_name='accounts/login.html', context=context)


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
        redirect('account:login')
    return render(request, template_name='accounts/register.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')


def guest_register_view(request):
    guest_form = GuestForm(request.POST or None)
    context = {
        'form': guest_form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if guest_form.is_valid():
        email = guest_form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(to=redirect_path)
        else:
            return redirect('account:register')
    return redirect(to='account:register')



