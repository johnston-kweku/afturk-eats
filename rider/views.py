from django.shortcuts import render
from accounts.decorators import role_required
from accounts.models import User
# Create your views here.

@role_required(User.Role.RIDER)
def rider_dashboard(request):
    return render(request, 'rider/dashboard.html')