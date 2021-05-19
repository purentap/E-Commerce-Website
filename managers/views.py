from django.shortcuts import redirect, render
from store.models import *
# Create your views here.

def productManager(request):
    context={}
    return render(request, "managers/index.html", context)

def pmTables(request):
    products = Product.objects.all()
    context={'products': products}
    return render(request, "managers/tables.html", context)

def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    products = Product.objects.all()
    context={'products': products}
    return render(request, "managers/tables.html", context)

