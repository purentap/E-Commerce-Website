from django.shortcuts import render
from register.forms import User
from django.core.mail import EmailMessage, send_mail
from mysite.settings import EMAIL_HOST_USER as mailer
from django.dispatch import receiver
from store.models import Order
from django.db.models.signals import post_save, pre_save
from .tasks import welcome_mail
# Create your views here.

# # New User Email # Will add HTML body
# @receiver(post_save, sender = User)
# def welcome_mail(sender, instance, created, **kwargs):
#     if created:
#         email = EmailMessage(
#             "WELCOME TO PWACK",
#             "Welcome to Pwack,\n We are happy to see you with us!\nSound ON!",
#             mailer,
#             [instance.email]
#         )
#         email.send()

@receiver(post_save, sender = User)
def welcome_mail_check(sender, instance, created, **kwargs):
    if created:
        lst = str(instance.email)
        
        
        # lst = [instance.email]
        # sent = str(mailer)
        welcome_mail.delay(lst)
        print("welcome")



# Order Confirm Invoice Email # Synchronous Version
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



# # # # # #
# import multiprocessing as mp

# def func(a,b,c,d):
#     # email.attach_file('data/pdfs/invoice_{}.pdf'.format(instance.transaction_id))
#     email = EmailMessage(a,b,c,d)
#     email.send()

# @receiver(post_save, sender = Order)
# def invoice_email_send(sender, instance, created, **kwargs):
#     if created == False:
#         if instance.isComplete == True:
#             # email = EmailMessage(
#             #     "Pwack Purchase Information",
#             #     "Thank you for your pwachase!,\nSee you again!",
#             #     str(mailer),
#             #     [str(instance.customer.email)]
#             # )
#             a = "Pwack Purchase Information"
#             b = "Thank you for your pwachase!,\nSee you again!"
#             c = str(mailer)
#             d = [str(instance.customer.email)]
#             data = mp.Process(
#                 target = func,
#                 args=(a,b,c,d)
#             )
#             data.start()
#             data.join(60)
