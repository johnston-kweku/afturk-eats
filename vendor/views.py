from django.shortcuts import render
from accounts.decorators import role_required
from accounts.models import User
# Create your views here.


@role_required(User.Role.VENDOR)
def vendor_dashboard(request):
    return render(request, 'vendor/vendor_dashboard.html')