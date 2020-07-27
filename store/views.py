from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
import datetime


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartTotalItems = order.get_total_items
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_items': 0, 'shipping': False}
        cartTotalItems = order['get_total_items']

    context = {'items': items, 'order': order}

    products = Product.objects.all()
    context = {'products': products, 'cartTotalItems': cartTotalItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartTotalItems = order.get_total_items
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_items': 0, 'shipping': False}
        cartTotalItems = order['get_total_items']

    context = {'items': items, 'order': order,
               'cartTotalItems': cartTotalItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartTotalItems = order.get_total_items
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_items': 0, 'shipping': False}
        cartTotalItems = order['get_total_items']

    context = {'items': items, 'order': order,
               'cartTotalItems': cartTotalItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('ProdectId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added to order', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['userForm']['total'])
        order.transaction_id = transaction_id

        if total == order.get_total_price:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Processing order...', safe=False)
