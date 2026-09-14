from django.db import models
from django.conf import settings
from order.models import Category


# Create your models here.

class VendorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    business_name = models.CharField(max_length=200)
    is_approved = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, related_name='vendor')
