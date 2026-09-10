from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from .decorators import role_required
from .models import Invitation, User
from .helpers import create_token
import json

# Create your views here.



def home(request):
    return render(request, 'accounts/index.html')


@role_required('ADMIN')
def generate_invite_link(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON structure.'
        }, status=400)

    role = data.get('role', '')
    if not role:
        return JsonResponse({
            'success': False,
            'message': 'Please provide a role.'
        }, status=400)

    if role not in User.Role.values:
        return JsonResponse({
            'success': False,
            'message': 'Invalid role.'
        }, status=400)

    invitation = create_token(request.user, role)

    invitation_link = request.build_absolute_uri(f'/register/?token={invitation.token}')

    return JsonResponse({
        'success': True,
        'message': 'Invitation link generated successfully.',
        'invitation_link': invitation_link
    })




def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')  

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'accounts/login.html', {'username': username})

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html', {'username': username})

        if not user.is_active:
            messages.error(request, 'This account has been deactivated. Contact support.')
            return render(request, 'accounts/login.html', {'username': username})

        login(request, user)

        # Role-based redirect
        if user.role == user.Role.RIDER:
            return redirect('rider:dashboard')
        elif user.role == user.Role.VENDOR:
            return redirect('vendor:dashboard')
        elif user.role == user.Role.CUSTOMER:
            return redirect('customer:home')
        elif user.role == user.Role.ADMIN:
            return redirect('admin:index')

        return redirect('accounts:dashboard')  # fallback

    return render(request, 'accounts/login.html', {'username': ''})



def logout_view(request):
    logout(request)
    return redirect('accounts:login')



def user_registration(request):
    if request.method == 'GET':
        token = request.GET.get('token', '')
        invitation = get_object_or_404(Invitation, token=token)
        if not token:
            return render(request, 'register/customer_registration.html')

        if not invitation:
            return 

