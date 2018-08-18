from django.db import models
# from order.models import Order
from meal.models import Meal
from account.models import CaterUser

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(CaterUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    meals = models.ManyToManyField(Meal, through='CartItems')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user.email


class CartItems(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.meal.name
