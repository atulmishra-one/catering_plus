from django.contrib import admin

from .models import Order
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'status', 'order_date', 'items')


    @classmethod
    def items(cls, obj):
        return "-".join(["{0}-{1}".format(g.meal.name, g.quantity) for g in obj.cart.cartitems_set.all()])



admin.site.register(Order, OrderAdmin)


