from django.shortcuts import render
from accounts.models import User, Invitation
from vendor.models import VendorProfile
from rider.models import RiderProfile

# Create your views here.


def admin_dashboard(request):
    vendor_applications = VendorProfile.objects.filter(
        is_approved=False,
        user__is_active=False
    ).order_by('') # Going to add a created at and updated at fields to help with ordering.

    rider_applications = RiderProfile.objects.filter(
        is_approved=False,
        user__is_active=False
    )


    return render(request, 'console/admin_dashboard.html')


def application_review(request): pass



def admin_settings(request):
    return render(request, 'console/settings.html')