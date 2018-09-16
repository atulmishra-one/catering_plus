from django.contrib import admin
from .models import Cart, CartItems
from django.utils.html import format_html

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart_name', 'active', 'date_added', 'cart_items')

    @classmethod
    def cart_name(cls, obj):
        return obj.user.email

    @classmethod
    def cart_items(cls, obj):
        items = u"<table class='field-cart-items-table'>"
        qty = 0
        price = 0
        for item in obj.meals.through.objects.all():
            items += u"<tr><td>{0}</td><td>Qty : {1}</td><td>Price : {2}</td></tr>".format(item, item.quantity,
                                                                                           item.meal.price)
            qty += item.quantity
            price += item.meal.price
        items += "<tfoot><tr><td>Total: </td><td>{0}</td><td>{1}</td></tr></tfoot>".format(qty, price)
        items += u"</table>"
        return format_html(items)

    class Media:
        css = {
            "screen": ("css/cart/cart.css", )
        }


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'meal', 'quantity', )


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)


