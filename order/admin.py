from django.contrib import admin

from .models import Order
from django.utils.html import format_html
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'status', 'order_date', 'items')

    @classmethod
    def items(cls, obj):
        items = u"<table class='field-items-table'>"
        qty = 0
        price = 0
        for item in obj.cart.cartitems_set.all():
            items += u"<tr><td>{0}</td><td>Qty : {1}</td><td>Price : {2}</td></tr>".format(item, item.quantity,
                                                                                           item.meal.price)
            qty += item.quantity
            price += item.meal.price
        items += "<tfoot><tr><td>Total: </td><td>{0}</td><td>{1}</td></tr></tfoot>".format(qty, price)
        items += u"</table>"
        return format_html(items)

    class Media:
        css = {
            "screen": ("css/order/order.css", )
        }


admin.site.register(Order, OrderAdmin)


