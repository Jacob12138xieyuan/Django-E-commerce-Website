import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_total_price': 0, 'get_total_items': 0, 'shipping': False}
    cartTotalItems = order['get_total_items']

    for productId in cart:
        try:
            cartTotalItems += cart[productId]['quantity']

            product = Product.objects.get(id=productId)
            total = (product.price * cart[productId]['quantity'])

            order['get_total_price'] += total
            order['get_total_items'] += cart[productId]['quantity']

            ordreItem = {  # fake orderItem model
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[productId]['quantity'],
                'get_total': total
            }
            items.append(ordreItem)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartTotalItems': cartTotalItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartTotalItems = order.get_total_items
    else:
        cookieData = cookieCart(request)
        cartTotalItems = cookieData['cartTotalItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartTotalItems': cartTotalItems, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['userForm']['name']
    email = data['userForm']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity']
        )
    return customer, order
