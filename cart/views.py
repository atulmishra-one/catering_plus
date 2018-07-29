from django.shortcuts import render, HttpResponse
import json
from .models import Cart
from meal.models import Meal
from django.contrib.auth.decorators import login_required
from collections import defaultdict

# Create your views here.


@login_required
def add_to_cart(request):
    code = 404
    content = {}
    if request.method == 'POST':
        meal = Meal.objects.get(pk=request.POST['meal_id'])
        try:
            pre_existing_cart = Cart.objects.get(user=request.user, meal=meal, active=True)
            pre_existing_cart.quantity += 1
            pre_existing_cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user=request.user,
                active=True,
                meal=meal,
                quantity=1
            )
            cart.save()
            print("Saving...")
        finally:
            code = 202
            cart = Cart.objects.filter(user=request.user, meal=meal, active=True).first()
            content = {'message': 'success', 'quantity': cart.quantity}
    return HttpResponse(status=code, content=json.dumps(content), content_type='application/json')


@login_required
def remove_from_cart(request):
    code = 404
    content = {}
    if request.method == 'POST':
        meal = Meal.objects.get(pk=request.POST['meal_id'])
        cart = Cart.objects.get(user=request.user, active=True, meal=meal)
        if not cart:
            Cart.objects.get(user=request.user).delete()
        cart.quantity -= 1
        cart.save()
        code = 200
        content = {
            'message': 'success'
        }
    return HttpResponse(status=code, content=json.dumps(content), content_type='application/json')


@login_required
def get_cart_item(request):
    carts = Cart.objects.filter(user=request.user).all()
    quantities = defaultdict(list)
    prices = defaultdict(list)
    for cart in carts:
        quantities[cart.meal.id].append(cart.quantity)
        prices[cart.meal.id].append(cart.meal.price)

    items_total = 0
    prices_total = 0
    for i, v in quantities.items():
        items_total += sum(v)
        prices_total += sum(v) * int(prices[i][0])

    content = [{'meal_name': cart.meal.name, 'meal_id': cart.meal.id, 'quantity': cart.quantity} for cart in carts]

    output = {
        'total': items_total,
        'content': content,
        'prices_total': prices_total
    }
    return HttpResponse(status=200, content=json.dumps(output), content_type='application/json')


@login_required
def view_cart(request):

    return render(request, 'view_cart.html')


