from django.db import models
from django.conf import settings
# Create your models here.




class RiderProfile(models.Model):
    class Vehicle(models.TextChoices):
        MOTORCYCLE = 'MOTORCYCLE', 'Motorcycle'
        BICYCLE = 'BICYCLE', 'Bicycle'
        CAR = 'CAR', 'Car'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )



    profile_image = models.ImageField(upload_to='riders/profile/')
    rented_vehicle = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    vehicle_type = models.CharField(max_length=20, choices=Vehicle.choices)
    ghana_card_number = models.CharField(max_length=20, unique=True)
    ghana_card_image = models.ImageField(upload_to='riders/ghana_cards/')
    is_student = models.BooleanField(default=False)
    student_id_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    last_seen_at = models.DateTimeField(null=True, blank=True)


