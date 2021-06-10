from celery import shared_task
import glob
import os
import io
from store.models import *
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail, send_mass_mail
from mysite.settings import EMAIL_HOST_USER as mailer
from django.core import serializers
from django.template.loader import get_template, render_to_string
from mail.utils import render_to_pdf
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from pathlib import Path
from email.mime.image import MIMEImage

@shared_task
def welcome_mail(lst, name):

    context = {'name' : name}

    html = render_to_string('mail/welcome.html', context)
    email = EmailMultiAlternatives()
    email.subject = "WELCOME TO PWACK"
    email.body = "welcome"
    email.from_email = mailer
    email.to = [lst]
    email.attach_alternative(html, "text/html")
    email.send()
    print("welcome 2")

@shared_task
def invoice_create_send(pk):
    number = pk
    order = Order.objects.get(pk=number)
    items = order.orderitem_set.all()
    customer = order.customer
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
    filename = "Pwack_Invoice_{}_{}_{}.pdf".format(customer.first_name, customer.last_name, order.id)
    email.attach(filename, pdf)
    email.send()

@shared_task
def discount_email(product, old_price):
    product = Product.objects.get(pk = product)
    # get all users in list
    User = get_user_model()
    users = User.objects.all()
    user_list = []
    for i in users:
        if i != None or i != '':
            user_list.append(i.email)
    print(user_list)


    context = {'product' : product, 'old_price' : old_price}


    html = render_to_string('mail/discount.html', context)

    email = EmailMultiAlternatives()
    email.subject = "PWACK HAS DISCOUNTS"
    email.body = "DISCOUNT"
    email.from_email = mailer
    email.bcc = user_list
    email.to = ['natansuslu@sabanciuniv.edu']
    email.attach_alternative(html, "text/html")

    email.send()