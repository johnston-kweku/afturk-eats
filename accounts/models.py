from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        RIDER = 'RIDER', 'Rider'
        VENDOR = 'VENDOR', 'Vendor'
        CUSTOMER = 'CUSTOMER', 'Customer'

    full_name = models.CharField(max_length=200, blank=False)
    role = models.CharField(max_length=50, choices=Role.choices)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True, blank=True)
    


