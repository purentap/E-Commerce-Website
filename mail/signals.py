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
# Create your views here.

@receiver(post_save, sender = User)
def welcome_mail_check(sender, instance, created, **kwargs):
    if created:
        lst = str(instance.email)
        
        
        # lst = [instance.email]
        # sent = str(mailer)
        welcome_mail.delay(lst)
        print("welcome")



# # Order Confirm Invoice Email # Synchronous Version
# @receiver(post_save, sender = Order)
# def invoice_email_send(sender, instance, created, **kwargs):
#     if created == False:
#         if instance.isComplete == True:
#             email = EmailMessage(
#                 "Pwack Purchase Information",
#                 "Thank you for your pwachase!,\nSee you again!",
#                 mailer,
#                 [instance.customer.email]
#             )
#             email.message()
#             # email.attach_file('data/pdfs/invoice_{}.pdf'.format(instance.transaction_id))
#             email.send()



# # Order Confirm Invoice Email # Asynchronous Version
# @receiver(post_save, sender = Order)
# def invoice_email_send(sender, instance, created, **kwargs):
#     if created == False:
#         if instance.isComplete == True:
#             pk = (instance.id)
#             invoice_create_send.delay(pk)

#             # invoice_create_send.delay(instance = instance.)
#             # email = EmailMessage(
#             #     "Pwack Purchase Information",
#             #     "Thank you for your pwachase!,\nSee you again!",
#             #     mailer,
#             #     [instance.customer.email]
#             # )
#             # email.message()
#             # # email.attach_file('data/pdfs/invoice_{}.pdf'.format(instance.transaction_id))
#             # email.send()

