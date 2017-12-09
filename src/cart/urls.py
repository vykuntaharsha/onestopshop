from django.conf.urls import url
from .views import cart_home, cart_update, checkout_home, checkout_done_view, cart_detail_api_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view

urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^api/$', cart_detail_api_view, name='cart-api'),
    url(r'^update/$', cart_update, name='update'),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    url(r'^checkout/success$',checkout_done_view, name='success'),
    url(r'^checkout/$',checkout_home, name='checkout'),

]
