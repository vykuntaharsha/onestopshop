from django.conf.urls import url
from .views import (LoginView, logout_view, RegisterView,
                    GuestRegisterView, AccountHomeView, AccountEmailActivateView,
                    UserDetailUpdateView)
from products.views import UserProductHistoryView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/guest/$', GuestRegisterView.as_view(), name='guest-register'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^details/$', UserDetailUpdateView.as_view(), name='user-update'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
    url(r'^email/resend-activation/$', AccountEmailActivateView.as_view(), name='resend-activation'),
    url(r'^$', AccountHomeView.as_view(), name='home'),
    url(r'history/products/$', UserProductHistoryView.as_view(), name='user-product-history'),
]
