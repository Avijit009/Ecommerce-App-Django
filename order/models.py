from django.db import models
from django.conf import settings

from shop.models import Product
# Create your models here.

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount = models.FloatField()
    min_amount = models.IntegerField(default=500)

    def __str__(self):
        return self.coupon_code

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.quantity} x {self.item}'
    
    def get_total(self):
        total = self.item.price * self.quantity
        priceTotal = format(total,'0.2f')
        return priceTotal

class Order(models.Model):
    Processing = 'Processing'
    Delivered = 'Delivered'
    status_choices = [
        (Processing, 'Processing'),
        (Delivered, 'Delivered')
    ]
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_coupon')
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=255,blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=status_choices, default=Processing)

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())

        if self.coupon and self.coupon.is_expired == False:
            if self.coupon.min_amount <= total:
                total = total - (total * (self.coupon.discount/100))
                return total

        return total