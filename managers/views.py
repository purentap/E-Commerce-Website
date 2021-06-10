from django.shortcuts import redirect, render
from store.models import *
from .forms import *
from mail.utils import render_to_pdf
from django.http import HttpResponse
from mysite.decorators import product_manager
# Create your views here.

@product_manager
def productManager(request):
    context={}
    return render(request, "managers/base.html", context)

@product_manager
def pmTables(request):
    products = Product.objects.all()
    context={'products': products}
    return render(request, "managers/tables.html", context)

@product_manager
def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    products = Product.objects.all()
    context={'products': products}
    return render(request, "managers/tables.html", context)

@product_manager
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

@product_manager
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

@product_manager
def comments(request):
    comments = Comment.objects.all()
    print(comments)
    context={'comments': comments}
    return render(request, "managers/comments.html", context)

@product_manager
def approve(request, id):
    comment = Comment.objects.get(id=id)
    comment.approval = 2
    comment.save()
    comments = Comment.objects.all()
    context={'comments': comments}
    return render(request, "managers/comments.html", context)

@product_manager
def disapprove(request, id):
    comment = Comment.objects.get(id=id)
    comment.approval = 3
    comment.save()
    comments = Comment.objects.all()
    context={'comments': comments}
    return render(request, "managers/comments.html", context)

@product_manager
def orders(request):
    orders = Order.objects.filter(isComplete=True).exclude(status=3)
    addresses = ShippingAdress.objects.all()
    context={'orders':orders, 'addresses':addresses}
    return render(request, "managers/orders.html", context)

@product_manager
def invoice(request, id):
    items = OrderItem.objects.filter(order=id)
    order = Order.objects.get(id=id)
    adress = ShippingAdress.objects.get(order=order)
    customer = order.customer
    total = 0
    for i in items:
        total += i.product.price * i.quantity
    context={'items': items, 'order':order, 'total':total, 'shipping':adress, 'customer' : customer}
    return render(request, "managers/invoice.html", context)

@product_manager
def changeStatus(request, id):
    order = Order.objects.get(id=id)
    if order.status == 1:
        order.status = 2
    elif order.status == 2:
        order.status = 3
    order.save()
    return redirect('/orders')

@product_manager
def viewPDF(request, id):
    number = id
    order = Order.objects.get(pk=number)
    items = order.orderitem_set.all()
    customer = order.customer
    shipping = ShippingAdress.objects.get(order = order)
    context={'items' : items, 'order' : order, 'shipping': shipping, 'customer' : customer}
    pdf = render_to_pdf('mail/index.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

@product_manager
def downloadPDF(request, id):
    number = id
    order = Order.objects.get(pk=number)
    items = order.orderitem_set.all()
    customer = order.customer
    shipping = ShippingAdress.objects.get(order = order)
    context={'items' : items, 'order' : order, 'shipping': shipping, 'customer' : customer}
    pdf = render_to_pdf('mail/index.html', context)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Pwack_Invoice_{}_{}_{}.pdf".format(customer.first_name, customer.last_name, order.transaction_id)
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    return response
