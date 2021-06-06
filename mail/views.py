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

# class ViewPDF(View):
#     def get(self, request, *args, **kwargs):
#         pdf = render_to_pdf('invoice.html', data)


# def generatePDF(order, items):
#     tID = order.transactionID
#     filename = "invoice_{}.pdf".format(tID)
#     context={'items' : items, 'order' : order}
#     template = get_template('invoice.html')
#     pdf = render_to_pdf
#     return filename