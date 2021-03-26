from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

user = get_user_model()


@receiver(post_save, sender=user)
def post_save_create_buyer(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)
