from django.db import transaction
from django.urls import reverse
from .models import Invitation, User
from customer.models import CustomerProfile
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


def get_dashboard_url(user):
    if user.role == User.Role.CUSTOMER:
        return reverse('customer:customer_dashboard')

    if user.role == User.Role.RIDER:
        return reverse('rider:rider_dashboard')

    if user.role == User.Role.VENDOR:
        return reverse('vendor:vendor_dashboard')

    return reverse('accounts:home')