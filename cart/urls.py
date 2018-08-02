from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='view_cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    path('get_cart_item', views.get_cart_item, name='get_cart_item'),
    path('make_payment', views.make_payment, name='make_payment')
]
