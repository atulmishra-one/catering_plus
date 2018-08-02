from django.shortcuts import HttpResponse, redirect
import json
from .models import Cart, CartItems
from meal.models import Meal, Category
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from order.models import Order
from datetime import datetime

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'view_cart.html'


@login_required
def add_to_cart(request):
    code = 404
    content = {}
    if request.method == 'POST':
        meal = Meal.objects.get(pk=request.POST['meal_id'])
        try:
            cart = Cart.objects.get(user=request.user, active=True)
            pre_existing_cart = CartItems.objects.get(meal=meal, cart=cart)
            pre_existing_cart.quantity += 1
            pre_existing_cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user=request.user,
                active=True
            )
            items = CartItems.objects.create(
                meal=meal,
                quantity=1,
                cart=cart
            )
            items.save()
            cart.cartitems_set.add(items)
            cart.save()
        except CartItems.DoesNotExist:
            items = CartItems.objects.create(
                meal=meal,
                quantity=1,
                cart=cart
            )
            items.save()
            cart.cartitems_set.add(items)
            cart.save()
        finally:
            code = 202
            cart = CartItems.objects.get(meal=meal, cart=cart)
            content = {'message': 'success', 'quantity': cart.quantity}
    return HttpResponse(status=code, content=json.dumps(content), content_type='application/json')


@login_required
def remove_from_cart(request):
    code = 404
    content = {}
    if request.method == 'POST':
        meal = Meal.objects.get(pk=request.POST['meal_id'])
        cart = Cart.objects.filter(user=request.user, active=True)[0]
        pre_existing_cart = CartItems.objects.get(meal=meal, cart=cart)
        if pre_existing_cart.quantity >= 1:
            pre_existing_cart.quantity -= 1
        cart.save()
        pre_existing_cart.save()
        code = 200
        content = {
            'message': 'success'
        }
    return HttpResponse(status=code, content=json.dumps(content), content_type='application/json')


@login_required
def get_cart_item(request):
    #cart = get_object_or_404(Cart, user=request.user, active=True)
    try:
        cart = Cart.objects.filter(user=request.user, active=True)[0]
    except IndexError:
        return HttpResponse(status=200, content=json.dumps([]), content_type='application/json')
    cart_items = cart.cartitems_set.all()
    quantities = defaultdict(list)
    prices = defaultdict(list)
    for cart in cart_items:
        quantities[cart.meal.id].append(cart.quantity)
        prices[cart.meal.id].append(cart.meal.price)

    items_total = 0
    prices_total = 0
    for i, v in quantities.items():
        items_total += sum(v)
        prices_total += sum(v) * int(prices[i][0])

    content = [{'meal_name': cart.meal.name, 'meal_id': cart.meal.id,
                'quantity': cart.quantity, 'price': int(cart.meal.price)} for cart in cart_items]

    output = {
        'total': items_total,
        'content': content,
        'prices_total': prices_total
    }
    return HttpResponse(status=200, content=json.dumps(output), content_type='application/json')

@login_required
def make_payment(request):
    try:
        cart = Cart.objects.filter(user=request.user, active=True)[0]
        order = Order.objects.create(cart=cart, order_date=datetime.today())
        cart.active = False
        cart.save()
        order.save()
    except IndexError:
        return redirect('/meals')
    return redirect('/cart')


