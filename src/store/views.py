import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import *
from django.core.paginator import Paginator


def store(request):
    
    Data = DataCart(request)
    cartItems = Data['cartItems']

    list_products = Product.objects.all()
    pages = Paginator(list_products, 6)
    pagina = request.GET.get("page")  or 1
    products = pages.get_page(pagina)
    current = int(pagina)
    total_pages = range(1, products.paginator.num_pages + 1)

    context = {"products":products, "cartItems": cartItems, 'total_pages':total_pages, 'current':current}
    return render(request, 'store.html', context)

def cart(request):
    
    Data = DataCart(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    
    Data = DataCart(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)

def UpdateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print(f'Action: {action}')
    print(f'productID: {productID}')

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item Añadido', safe=False)

def ProcessOrder(request):
    data = json.loads(request.body)
    transaction = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transition_id = transaction

    if total == float(order.get_Total_Cart):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['userAddress']['address'],
            city = data['userAddress']['city'],
            state = data['userAddress']['state'],
            zipcode = data['userAddress']['zipcode'],
        )


    return JsonResponse('Pago Realizado', safe=False)