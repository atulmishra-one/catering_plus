from django.db import models
from cart.models import Cart

# Create your models here.


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    PENDING = 0
    WAITING_PAYMENT = 1
    PAYMENT_DONE = 2
    PREPARING = 3
    COMPLETE = 4
    CANCELLED = 5
    STATUS = (
        (PENDING, 'Pending'),
        (WAITING_PAYMENT, 'Waiting payment'),
        (PAYMENT_DONE, 'Payment done'),
        (PREPARING, 'Preparing'),
        (COMPLETE, 'Complete'),
        (CANCELLED, 'Cancelled')
    )
    status = models.SmallIntegerField(choices=STATUS, default=PENDING)

    def __str__(self):
        return self.cart.user.email

    class Meta:
        ordering = ['-order_date']
