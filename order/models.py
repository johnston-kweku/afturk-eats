from django.db import models
from customer.models import CustomerProfile
from vendor.models import VendorProfile
from rider.models import RiderProfile

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

    

    customer = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.SET_NULL)
    rider = models.ForeignKey(RiderProfile, on_delete=models.SET_NULL, null=True)
    order_type = models.CharField(max_length=30, choices=OrderType.choices)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.ONLINE)
    