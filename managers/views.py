from django.shortcuts import redirect, render
from store.models import *
from .forms import *
# Create your views here.

def productManager(request):
    context={}
    return render(request, "managers/base.html", context)

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

def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
		#print('Printing POST:', request.POST)
	    form = ProductForm(request.POST, request.FILES)
	    if form.is_valid():
		    form.save()
		    return redirect('/tables')
    context={'form': form}
    return render(request, "managers/product_form.html", context)

def updateStock(request):
    if request.method=="POST":
        id = request.POST['product']
        stock = int(request.POST['stock'])
        product = Product.objects.get(pk=id)
        product.stock = stock
        product.save()
        products = Product.objects.all()
        context={'products': products}
        return render(request, "managers/tables.html", context)

def comments(request):
    comments = Comment.objects.all()
    print(comments)
    context={'comments': comments}
    return render(request, "managers/comments.html", context)