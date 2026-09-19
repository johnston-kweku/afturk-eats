from django.db import models
from django.conf import settings
from django.utils import timezone
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
    is_online = models.BooleanField(default=False)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name

    def is_currently_open(self):
        if not self.is_online:
            return False

        now = timezone.localtime()
        today_hours = self.opening_hours.filter(day=now.weekday()).first()

        if not today_hours or today_hours.is_closed:
            return False

        return today_hours.open_time <= now.time() <= today_hours.close_time

class MenuItem(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='menu_items')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.vendor.business_name})"




class MenuItemVariant(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='variants')
    label = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.menu_item.name} - {self.label} (₵{self.price})"
    

    


class OpeningHours(models.Model):
    class Day(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='opening_hours')
    day = models.IntegerField(choices=Day.choices)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('vendor', 'day')
        ordering = ['day']

    def __str__(self):
        return f"{self.get_day_display()} — {self.vendor.business_name}"

