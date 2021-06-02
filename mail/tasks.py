from celery import shared_task
import glob
import os
import io
from store.models import *
from django.core.mail import EmailMessage
from mysite.settings import EMAIL_HOST_USER as mailer

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
