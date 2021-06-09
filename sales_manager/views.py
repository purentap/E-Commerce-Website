from django.shortcuts import redirect, render
from store.models import *
from mysite.decorators import sales_manager
from mail.utils import render_to_pdf
from django.http import HttpResponse
from datetime import datetime, timezone
# Create your views here.

@sales_manager
def salesManager(request):
    products = Product.objects.all()
    context={'products': products}
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

@sales_manager
def orders(request):
    orders = Order.objects.filter(isComplete=True)
    addresses = ShippingAdress.objects.all()
    context={'orders':orders, 'addresses':addresses}
    return render(request, "sales_manager/orders.html", context)

@sales_manager
def viewPDF(request, id):
    number = id
    order = Order.objects.get(pk=number)
    items = order.orderitem_set.all()
    customer = order.customer
    shipping = ShippingAdress.objects.get(order = order)
    context={'items' : items, 'order' : order, 'shipping': shipping, 'customer' : customer}
    pdf = render_to_pdf('mail/index.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

@sales_manager
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

@sales_manager
def chart(request):
    date_entered=0
    purchases = OrderItem.objects.filter(refund_request=False)
    profit_sum = 0
    for item in purchases:
        profit_sum += item.product.price

    refunds = Refund.objects.filter(approval=2)
    loss_sum = 0
    for refund in refunds:
        loss_sum += refund.price
    revenue = profit_sum - loss_sum
    context={"loss":loss_sum, "profit":profit_sum, "revenue":revenue, "date_entered":date_entered}
    return render(request, "sales_manager/charts.html", context)

@sales_manager
def setDates(request):
    if request.method=="POST":
        date_entered=1
        start_date = request.POST['start-date']
        end_date =request.POST['end-date']
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        purchases = OrderItem.objects.filter(refund_request=False)
        profit_sum = 0
        for item in purchases:
            if item.order.order_date.date() > start.date() and item.order.order_date.date() < end.date():
                profit_sum += item.product.price

        refunds = Refund.objects.filter(approval=2 )
        loss_sum = 0
        for refund in refunds:
            if refund.request_date.date() > start.date() and refund.request_date.date() < end.date():
                loss_sum += refund.price
        revenue = profit_sum - loss_sum
        context={"loss":loss_sum, "profit":profit_sum, "revenue":revenue, "date_entered":date_entered, "start":start.date(), "end":end.date()}
        return render(request, "sales_manager/charts.html", context)

@sales_manager
def invoiceDates(request):
    if request.method=="POST":
        start_date = request.POST['start-date']
        end_date =request.POST['end-date']
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        all_orders = Order.objects.filter(isComplete=True)
        orders = []
        for order in all_orders:
            if order.order_date.date() > start.date() and order.order_date.date() < end.date():
                orders.append(order)

        context={'orders':orders}
        return render(request, "sales_manager/orders.html", context)