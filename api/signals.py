from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
def create_user_token_on_registration(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
post_save.connect(receiver=create_user_token_on_registration, sender=get_user_model())