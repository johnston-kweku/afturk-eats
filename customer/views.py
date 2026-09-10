from django.shortcuts import render
from accounts.decorators import role_required
from accounts.models import User

# Create your views here.

@role_required(User.Role.CUSTOMER)
def customer_dashboard(request):
    return render(request, 'customer/customer_dashboard.html')