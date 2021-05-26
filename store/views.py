from django.shortcuts import redirect, render
from .models import *
from django.http import JsonResponse,HttpResponse
import json
from django.db.models import Q
from django.contrib import messages
import datetime
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

def category(request,category):
    products = Product.objects.filter(genre__iexact=category)
    context={'products': products}
    return render(request, 'store/category.html', context)

def sortPrice(request):
    products = Product.objects.filter().order_by('price')
    context={'products': products}
    return render(request, 'store/sortPrice.html', context)

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
    if request.user.is_authenticated:
        return redirect('profile')
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
    #transaction_id = 
    customer = request.user
    order = Order.objects.get(customer = customer, isComplete = False)
    data = json.loads(request.body)
    shippingForm = data['shippingForm']
    print(shippingForm)
    billingForm = data['billingForm']
    
    shipping, created = ShippingAdress.objects.get_or_create(customer = customer) # get_or_create veya düz create
    shipping.address = shippingForm['address']
    shipping.city = shippingForm['city']
    shipping.state = shippingForm['state']
    shipping.zipcode = shippingForm['zipcode']
    shipping.country = shippingForm['country']
    shipping.order = order

    shipping.save()

    billing, created = CreditCard.objects.get_or_create(customerID = customer)
    billing.cardName = billingForm['ownerName']
    billing.cardNumber = billingForm['CardNo']
    billing.exprDate = billingForm['ExpirationDate']

    billing.save()

    order.isComplete = True
    order.save()

    items =  order.orderitem_set.all()
    for i in items: ##DECREASE THE STOCK OF PURCHASED ITEMS
        i.product.stock = i.product.stock - i.quantity
        print(i.product.stock)
        i.product.save()

    return JsonResponse("Payment Complete", safe=False)

def successfulPayment(request):
    context={}
    return render(request, "store/successful.html", context)

    

def profile(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    context={}
    return render(request, "store/profile.html", context)


def addComment(request):
    
    if request.user.is_authenticated:
        if request.method=="POST":
            customer = request.user
            id = request.POST['product']
            product = Product.objects.get(pk=id)
            comment_body = request.POST['userComment']
            comment = Comment(product = product, user=customer, body = comment_body )
            comment.save()
            messages.success(request, 'Hello world.')
            context={'product': product}
            return render(request, "store/product.html", context)
        #return HttpResponse(res)

    
    else:
        #context={'product': product}
        #messages.add_message(request, messages.INFO, 'Hello world.')
        return render(request, "store/product.html", context)
    
def addRating(request):
    #this may be unnecessary
    product = Product.objects.filter(score=0).order_by("?").first()
    context = {'product': product}
    return render(request, "store/product.html", context)
    


