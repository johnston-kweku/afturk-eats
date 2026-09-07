from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string


# Create your models here.

class User(AbstractUser):
    # username, password inherited as-is — used for login

    class Role(models.TextChoices):
        RIDER = 'RIDER', 'Rider'
        VENDOR = 'VENDOR', 'Vendor'
        CUSTOMER = 'CUSTOMER', 'Customer'
        ADMIN = 'ADMIN', 'Admin'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=Role.choices)
    phone_number = models.CharField(max_length=15, unique=True)  # mandatory
    email = models.EmailField(unique=True, null=True, blank=True)  # optional
    date_of_birth = models.DateField(null=True, blank=True)
    public_id = models.CharField(max_length=12, unique=True, editable=False, blank=True)

    ROLE_PREFIX = {
        Role.RIDER: "RID",
        Role.VENDOR: "VEN",
        Role.CUSTOMER: "CUS",
        Role.ADMIN: "ADM",
    }

    def save(self, *args, **kwargs):
        if not self.public_id:
            prefix = self.ROLE_PREFIX.get(self.role, "USR")
            while True:
                suffix = "".join(random.choices(string.digits, k=6))
                candidate = f"{prefix}-{suffix}"
                if not User.objects.filter(public_id=candidate).exists():
                    self.public_id = candidate
                    break
        super().save(*args, **kwargs)
