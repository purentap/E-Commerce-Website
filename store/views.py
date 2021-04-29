from django.shortcuts import render
from .models import *
from django.http import JsonResponse,HttpResponse
import json
from django.db.models import Q
# Create your views here.

def store(request):
    products = Product.objects.all()
    context={'products': products}
    return render(request, "store/store.html", context)

def search(request):
    q = request.GET['q']
    products = Product.objects.filter(Q(album_name__icontains=q) | Q(artist_name__icontains=q))
    context={'products': products}
    return render(request, 'store/search.html', context)

def product_detail(request,id):
    product = Product.objects.get(pk=id)
    context={'product': product}
    return render(request, "store/product.html", context)

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(customer = user, isComplete= False)
        items = order.orderitem_set.all()
    
    else: #These are not stored in our database. Nonusers can see these products in their cart page
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}
        #print('Cart:', cart)
        items = []    
        order = {'getCartTotal' : 0 , 'getCartItems' : 0, 'isComplete' : False} #THIS IS JUST TEMPLATE. WILL CHANGE WHEN WE HANDLE NONUSER CART PART
        cartItems = order["getCartItems"]
        for i in cart:
            try:
                cartItems += cart[i]["quantity"]
                product = Product.objects.get(id = i)
                cost = (product.price *cart[i]["quantity"] )
                order['getCartTotal'] += cost
                order['getCartItems'] += cart[i]["quantity"]
                item = {
                    'product' : {
                        'id' : product.id,
                        'album_name' : product.album_name,
                        'artist_name' : product.artist_name,
                        'price' : product.price,
                        'image' : product.image,
                    },
                    'quantity': cart[i]["quantity"],
                    'getTotal' : cost
                }
                items.append(item)
            except: 
                pass
    context={'items' : items, 'order' : order}
    return render(request, "store/cart.html", context)

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(customer = user, isComplete= False)
        items = order.orderitem_set.all()
    else:
        cart = json.loads(request.COOKIES['cart'])
        items=[] #KEEP THESE EMPTY FOR NOW. WILL UPDATE LATER ON 
        order = {'getCartTotal' : 0 , 'getCartItems' : 0, 'isComplete' : False}
        cartItems = order["getCartItems"]
        for i in cart:
            try:
                cartItems += cart[i]["quantity"]
                product = Product.objects.get(id = i)
                cost = (product.price *cart[i]["quantity"] )
                order['getCartTotal'] += cost
                order['getCartItems'] += cart[i]["quantity"]
                item = {
                    'product' : {
                        'id' : product.id,
                        'album_name' : product.album_name,
                        'artist_name' : product.artist_name,
                        'price' : product.price,
                        'image' : product.image,
                    },
                    'quantity': cart[i]["quantity"],
                    'getTotal' : cost
                }
                items.append(item)
            except: 
                pass

    context={'items' : items, 'order' : order}
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

def processedPayment(request):
    print("DATA: " , request.body)
    return JsonResponse("Payment Complete", safe=False)

def successfulPayment(request):
    context={}
    return render(request, "store/successful.html", context)

def profile(request):
    context={}
    return render(request, "store/profile.html", context)