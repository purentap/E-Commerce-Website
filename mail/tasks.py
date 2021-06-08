from celery import shared_task
import glob
import os
import io
from store.models import *
from django.core.mail import EmailMessage, EmailMultiAlternatives
from mysite.settings import EMAIL_HOST_USER as mailer
from django.core import serializers
from django.template.loader import get_template, render_to_string
from mail.utils import render_to_pdf
from django.utils.html import strip_tags

@shared_task
def welcome_mail(lst):
    
    email = EmailMessage(
        "WELCOME TO PWACK",
        "Welcome to Pwack,\n We are happy to see you with us!\nSound ON!",
        mailer,
        [lst]
    )
    email.send()
    print("welcome 2")

@shared_task
def invoice_create_send(pk):
    number = pk
    order = Order.objects.get(pk=number)
    items = order.orderitem_set.all()
    customer = order.customer
    user_id = customer.id
    print(user_id)
    # User.objects.get(id = order.customer) # Get user email
    shipping = ShippingAdress.objects.get(order = order)
    context={'items' : items, 'order' : order, 'shipping': shipping, 'customer' : customer}
    # template = get_template('mail/thankyou.html').render()
    pdf = render_to_pdf("mail/index.html", context)
    print("wow")
    
    
    html = render_to_string('mail/thankyou.html', context)
    email = EmailMultiAlternatives()
    email.subject = "Pwack Purchase Confirmation"
    email.body = "TEST"
    email.from_email = mailer
    email.to = [customer.email]
    email.attach_alternative(html, "text/html")
    email.attach('invoice.pdf', pdf)
    email.send()
