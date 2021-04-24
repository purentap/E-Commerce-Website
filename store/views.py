from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.

def store(request):
    products = Product.objects.all()
    context={'products': products}
    return render(request, "store/store.html", context)

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(customer = user, isComplete= False)
        items = order.orderitem_set.all()
    
    else:
        items = []    
    
    context={'items' : items}
    return render(request, "store/cart.html", context)

def checkout(request):
    context={}
    return render(request, "store/checkout.html", context)

def account(request):
    context={}
    return render(request, "store/account.html", context)


def userUpdateItemInCart(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer = customer, isComplete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        order_item.quantity = order_item.quantity +1
    elif action == 'remove':
        order_item.quantity = order_item.quantity -1
    
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse("Item is added", safe = False)