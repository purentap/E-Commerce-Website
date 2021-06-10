from django.shortcuts import render
from register.forms import User
from django.core.mail import EmailMessage, send_mail
from mysite.settings import EMAIL_HOST_USER as mailer
from django.dispatch import receiver
from store.models import Order
from django.db.models.signals import post_save, pre_save
from mail.tasks import welcome_mail, invoice_create_send
from django.core import serializers
from django.forms.models import model_to_dict
import json
import api.serializers as s
from django.template.loader import get_template
from .utils import render_to_pdf
# Create your views here.

def generatePDF(context):
    template = get_template('invoice.html')
    pdf = render_to_pdf('invoice.html', context)
    return 
    


@receiver(post_save, sender = User)
def welcome_mail_check(sender, instance, created, **kwargs):
    if created:
        lst = str(instance.email)
        name = str(instance.first_name)
        welcome_mail.delay(lst, name)
        print("welcome")

# Order Confirm Invoice Email # Asynchronous Version
@receiver(post_save, sender = Order)
def invoice_email_send(sender, instance, created, **kwargs):
    if created == False:
        if instance.isComplete == True:
            pk = (instance.id)
            invoice_create_send.delay(pk)

