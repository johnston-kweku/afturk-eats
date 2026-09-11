from django.db import transaction
from django.urls import reverse
from .models import Invitation, User
from rider.models import RiderProfile
from customer.models import CustomerProfile
from vendor.models import VendorProfile
import re

def create_token(created_by, role):
    invitation = Invitation.objects.create(
        role=role,
        created_by=created_by
    )
    return invitation


def validate_ghana_card(number):
    pattern = r'^GHA-\d{9}-\d$'
    if re.match(pattern, number):
        return True
    return False


def _handle_customer_sign_up(username, password, first_name, last_name, phone_number, email=None):
    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            role=User.Role.CUSTOMER,
        )
        customer_profile = CustomerProfile.objects.create(user=user)
    return user


def _handle_rider_sign_up(
        username, 
        password, 
        first_name, 
        last_name, 
        phone_number, 
        profile_image, 
        ghana_card_image,
        ghana_card_number,
        is_student,
        vehicle_type,
        date_of_birth,
        rented_vehicle,
        student_id_number=None,
        email=None
                          ):
    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            role=User.Role.RIDER,
            is_active=False
        )
        rider_profile = RiderProfile.objects.create(
            user=user,
            profile_image=profile_image,
            ghana_card_image=ghana_card_image,
            ghana_card_number=ghana_card_number,
            is_student=is_student,
            student_id_number=student_id_number,
            vehicle_type=vehicle_type,
            date_of_birth=date_of_birth,
            rented_vehicle=rented_vehicle
        )

    return user, rider_profile


def _handle_vendor_sign_up(
        username,
        password, 
        first_name, 
        last_name, 
        phone_number, 
        profile_image, 
        ghana_card_image,
        ghana_card_number,
        business_name,
        category,
        date_of_birth,
        email=None
        ):
    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=User.Role.VENDOR,
            email=email,
            is_active=False
        )

        vendor_profile = VendorProfile.objects.create(
            user=user,
            profile_image=profile_image,
            ghana_card_number=ghana_card_number,
            ghana_card_image=ghana_card_image,
            business_name=business_name,
            category=category,
            date_of_birth=date_of_birth,
        )

    return user, vendor_profile

def get_dashboard_url(user):
    if user.role == User.Role.CUSTOMER:
        return reverse('customer:customer_dashboard')

    if user.role == User.Role.RIDER:
        return reverse('rider:rider_dashboard')

    if user.role == User.Role.VENDOR:
        return reverse('vendor:vendor_dashboard')

    return reverse('accounts:home')