from django.shortcuts import render
from accounts.models import User, Invitation
from vendor.models import VendorProfile
from rider.models import RiderProfile

# Create your views here.


def admin_dashboard(request):
    return render(request, 'console/admin_dashboard.html')