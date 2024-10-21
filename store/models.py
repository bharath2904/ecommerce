from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(default=timezone.now)

    @property
    def get_cart_total(self):
        total = sum([item.get_total for item in self.orderitem_set.all()])
        return total

    @property
    def get_cart_items(self):
        items = sum([item.quantity for item in self.orderitem_set.all()])
        return items


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.quantity for item in orderitems)
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
