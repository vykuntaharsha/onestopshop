from django.conf.urls import url
from .views import login_page, logout_view, register_page, guest_register_view

urlpatterns = [
    url(r'^login/$', login_page, name='login'),
    url(r'^register/guest/$', guest_register_view, name='guest-register'),
    url(r'^register/$', register_page, name='register'),
    url(r'^logout/$', logout_view, name='logout')

]
