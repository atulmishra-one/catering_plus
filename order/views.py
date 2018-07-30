from django.shortcuts import render
from django.views.generic import ListView
from .models import Order
from meal.models import Category
from cart.models import Cart


class OrderView(ListView):
    template_name = 'order_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        categories = Category.objects.all()
        breadcrumb = Category.objects.filter(parent=None).all()
        self.kwargs.update({'categories': categories, 'breadcrumb': breadcrumb, 'object_list': self.get_queryset()})
        return self.kwargs

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user).all()
        order = Order.objects.filter(cart__in=cart).all()
        return order



