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
    ghana_card_number = models.CharField(max_length=15, unique=True)
    ghana_card_image = models.ImageField(upload_to='vendor/ghana_cards/')
    profile_image = models.ImageField(upload_to='vendor/profile/')
    category = models.ManyToManyField(Category, related_name='vendor')
