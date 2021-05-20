from django.shortcuts import render
from store.models import *
# Create your views here.
def salesManager(request):
    products = Product.objects.all()
    context={'products': products}
    print("ZAAAAAAAAAA")
    return render(request, "sales_manager/sales-manager.html", context)


def discountProduct(request):
    if request.method=="POST":
            id = request.POST['product']
            print(id)
            discount = int(request.POST['discount'])
            product = Product.objects.get(pk=id)
            product.price = product.price - product.price * (discount/100)
            product.onDiscount = True
            product.save()

            products = Product.objects.all()
            context={'products': products}
            return render(request, "sales_manager/sales-manager.html", context)


def updatePrice(request):
    if request.method=="POST":
        id = request.POST['product']
        print(id)
        price = int(request.POST['price'])
        product = Product.objects.get(pk=id)
        product.price = price
        product.onDiscount = False
        product.save()
        products = Product.objects.all()
        context={'products': products}
        return render(request, "sales_manager/sales-manager.html", context)