from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string
import uuid




# Create your models here.

class User(AbstractUser):

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
    public_id = models.CharField(max_length=12, unique=True, editable=False, blank=True)

    ROLE_PREFIX = {
        Role.RIDER: "RID",
        Role.VENDOR: "VEN",
        Role.CUSTOMER: "CUS",
        Role.ADMIN: "ADM",
    }

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_rider(self):
        return self.role == self.Role.RIDER

    def is_vendor(self):
        return self.role == self.Role.VENDOR

    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    def save(self, *args, **kwargs):
        if not self.public_id:
            prefix = self.ROLE_PREFIX.get(self.role, "USR")
            while True:
                suffix = "".join(random.choices(string.digits, k=6))
                candidate = f"{prefix}-{suffix}"
                if not User.objects.filter(public_id=candidate).exists():
                    self.public_id = candidate
                    break
        self.email = self.email.strip() or None if self.email else None

        super().save(*args, **kwargs)


def default_expiry():
    return timezone.now() + timedelta(hours=48)



class Invitation(models.Model):
    token = models.UUIDField(unique=True, default=uuid.uuid4)
    role = models.CharField(max_length=20, choices=User.Role.choices)
    is_used = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)
    used_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()