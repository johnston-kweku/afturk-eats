from django.contrib import admin
from .models import VendorProfile


# Register your models here.


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'business_name', 'is_approved'
    ]

    list_editable = [
        'is_approved'
    ]