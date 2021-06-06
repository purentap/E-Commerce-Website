from django.shortcuts import redirect, render
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

def refund(request):
    refunds = Refund.objects.filter(approval=1)
    context={'refunds': refunds}
    return render(request, "sales_manager/refunds.html", context)

def approve(request, id):
    refund = Refund.objects.get(id=id)
    refund.approval = 2
    refund.save()
    item = Product.objects.get(id=refund.order_item.product.id)
    item.stock += 1
    item.save()
    return redirect('/refunds')

def disapprove(request, id):
    refund = Refund.objects.get(id=id)
    refund.approval = 3
    refund.save()
    return redirect('/refunds')
