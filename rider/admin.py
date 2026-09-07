from django.contrib import admin
from .models import RiderProfile
# Register your models here.

@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ghana_card_number', 'is_student', 'vehicle_type', 'rented_vehicle', 'is_approved')
    list_filter = ('is_approved', 'is_student', 'vehicle_type', 'rented_vehicle')
    search_fields = ('user__email', 'user__phone_number', 'ghana_card_number', 'student_id_number')
    list_editable = ('is_approved',)