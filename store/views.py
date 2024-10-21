from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *


def store(request):
    products = Product.objects.all()
    cartItems = 0

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        cartItems = order.get_cart_items

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = 0

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)



def checkout(request):
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = 0

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

from django.contrib.auth.models import User

def develop(request):
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = 0

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/development.html', context)


