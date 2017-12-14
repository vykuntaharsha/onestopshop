from django.conf.urls import url
from .views import LoginView, logout_view, RegisterView, guest_register_view

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/guest/$', guest_register_view, name='guest-register'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^logout/$', logout_view, name='logout')

]
