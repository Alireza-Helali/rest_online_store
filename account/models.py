from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

import os
import uuid


# Create your models here.

def image_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    final_name = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profile-images/', final_name)


class UserManager(BaseUserManager):
    """Manager for user model"""

    def create_user(self, email, password=None, **extra_fields):
        """creating and saving new user"""
        if not email:
            raise ValueError('users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """creating and saving new super user"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Profile(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    image = models.ImageField(upload_to=image_file_path, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner)


class Supplier(models.Model):
    store_name = models.CharField(max_length=25, default=" ")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.store_name


class Address(models.Model):
    STATE = [
        ('tehran', 'تهران'),
        ('khouzestan', 'خوزستان'),
        ('ardebil', 'اردبیل')
    ]
    state = models.CharField(max_length=20, choices=STATE, verbose_name="استان")
    city = models.CharField(max_length=20, verbose_name="شهر")
    street = models.CharField(max_length=20, verbose_name="خیابان")
    alley = models.CharField(max_length=20, verbose_name="کوچه")
    plate = models.IntegerField(verbose_name="پلاک")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    priority = models.SmallIntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
