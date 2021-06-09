from django.shortcuts import redirect, render
from store.models import *
from mysite.decorators import sales_manager
# Create your views here.

@sales_manager
def salesManager(request):
    products = Product.objects.all()
    context={'products': products}
    print("ZAAAAAAAAAA")
    return render(request, "sales_manager/sales-manager.html", context)

@sales_manager
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

@sales_manager
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

@sales_manager
def refund(request):
    refunds = Refund.objects.filter(approval=1)
    context={'refunds': refunds}
    return render(request, "sales_manager/refunds.html", context)

@sales_manager
def approve(request, id):
    refund = Refund.objects.get(id=id)
    refund.approval = 2
    refund.save()
    item = Product.objects.get(id=refund.order_item.product.id)
    item.stock += 1
    item.save()
    return redirect('/refunds')

@sales_manager
def disapprove(request, id):
    refund = Refund.objects.get(id=id)
    refund.approval = 3
    refund.save()
    return redirect('/refunds')
