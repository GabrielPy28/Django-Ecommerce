import json
from .models import *

def CookiesCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])

    except:
        cart = {}
    
    print(f'Cart: {cart}')
    items = []
    order = {'get_Total_Cart':0, 'get_items_Cart':0, 'shipping':False}
    cartItems = order['get_items_Cart']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_Total_Cart'] += total
            order['get_items_Cart'] += cart[i]['quantity']

            item = {
                'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_Total': total
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order':order, 'items':items}

def DataCart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_items_Cart   
    else:
        data = CookiesCart(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

    return {'cartItems': cartItems, 'order':order, 'items':items}

def guestOrder(request, data):
    print('Usuario No Registrado')
    print(f'Cookies: {request.COOKIES}')
        
    name = data['form']['name']
    email = data['form']['email']

    cookies = CookiesCart(request)
    items = cookies['items']

    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )

    return customer, order