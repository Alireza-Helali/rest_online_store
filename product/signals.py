from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from account.models import Supplier


@receiver(post_save, sender=Supplier)
def post_save_supplier(sender, instance, created, **kwargs):
    if created:
        user = get_user_model().objects.get(email=instance.user)
        user.is_supplier = True
        user.save()
