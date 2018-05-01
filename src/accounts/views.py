from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, GuestForm, ReactivateEmailForm, UserDetailChangeForm
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import GuestEmail, EmailActivation
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin
from django.conf import settings
from mainwebsite.mixins import NextUrlMixin, RequestFormAttachMixin

# Create your views here.

User = get_user_model()
LOGIN_URL = getattr(settings, 'LOGIN_URL', '/account/login')


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/account/login/'


def logout_view(request):
    logout(request)
    return redirect('/')


class GuestRegisterView(NextUrlMixin,  RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/account/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = "accounts/home.html"

    def get_object(self, **kwargs):
        return self.request.user


class AccountEmailActivateView(FormMixin, View):
    success_url = LOGIN_URL
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, 'your email has been confirmed. Please login.')
                return redirect('account:login')
            else:
                activated_qs = qs.filter(key__iexact=key, activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password:password_reset')

                    msg = f""" your email has already been confirmed. 
                    Do you need to <a href='{reset_link}'>reset your password? </a> """

                    messages.success(request, message=mark_safe(msg))
                    return redirect('account:login')
        context = {'form': self.get_form(), 'key':key}
        return render(request, template_name='registration/activation_error.html', context=context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = f'Activation link sent, please check your email.'
        messages.success(request=self.request, message=msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        return render(self.request, 'registration/activation-error.html', context)


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data()
        context['title'] = 'Change Your Account Details'
        return context

    def get_success_url(self):
        return reverse("account:home")