from django.db import models
from customer.models import CustomerProfile
from vendor.models import VendorProfile, MenuItemVariant
from rider.models import RiderProfile
import string
import random

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Categories'




class Order(models.Model):
    class OrderType(models.TextChoices):
        FOOD = 'FOOD', 'Food'

    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        DECLINED = 'DECLINED', 'Declined'
        PREPARING = 'PREPARING', 'Preparing'
        READY = 'READY', 'Ready'
        PICKED_UP = 'PICKED UP', 'Picked Up'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class PaymentMethod(models.TextChoices):
        ONLINE = 'ONLINE', 'Online'
        ON_DELIVERY = 'ON DELIVERY', 'On Delivery'

    customer = models.ForeignKey(CustomerProfile, on_delete=models.PROTECT)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.PROTECT)
    rider = models.ForeignKey(RiderProfile, on_delete=models.PROTECT)
    order_type = models.CharField(max_length=30, choices=OrderType.choices)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.ONLINE)
    delivery_code = models.CharField(max_length=6, blank=True, editable=False, unique=True)
    order_id = models.CharField(max_length=12, blank=True, editable=False, unique=True)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.customer.user.first_name} - {self.order_id}'

    def save(self, *args, **kwargs):
        if not self.order_id:
            prefix = 'ORD'
            while True:
                suffix = "".join(random.choices(string.digits, k=6))
                candidate = f'{prefix}-{suffix}'
                if not Order.objects.filter(order_id=candidate).exists():
                    self.order_id = candidate
                    break

        if not self.delivery_code:
            while True:
                code = "".join(random.choices(string.digits, k=4))
                if not Order.objects.filter(delivery_code=code).exists():
                    self.delivery_code = code
                    break

        super().save(*args, **kwargs)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='item')
    menu_item_variant = models.ForeignKey(MenuItemVariant, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    price_at_order_time = models.DecimalField


    def __str__(self):
        return self.order