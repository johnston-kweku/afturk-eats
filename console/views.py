from django.shortcuts import render
from accounts.models import User, Invitation
from vendor.models import VendorProfile
from rider.models import RiderProfile

# Create your views here.


def admin_dashboard(request):
    return render(request, 'console/admin_dashboard.html')


def application_review(request): pass



def admin_settings(request):
    return render(request, 'console/settings.html')