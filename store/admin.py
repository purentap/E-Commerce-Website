from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAdress)
admin.site.register(CreditCard)
admin.site.register(Comment)
admin.site.register(Refund)
