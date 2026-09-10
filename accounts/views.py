from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from .decorators import role_required
from .models import Invitation, User
from .helpers import (
    create_token, 
    _handle_customer_sign_up, 
    get_dashboard_url, 
    _handle_rider_sign_up, 
    validate_ghana_card
)
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

    customer_template_path = 'register/customer_registration.html'
    rider_template_path = 'register/rider_registration.html'
    vendor_template_path = 'register/vendor_registration.html'

    if request.method == 'GET':
        token = request.GET.get('token', '')
        invitation = get_object_or_404(Invitation, token=token)
        if not token:
            return render(request, customer_template_path)


        if not invitation.is_valid():
            return redirect('accounts:invalid_invite')

        context = {'token', token}
        registration_role = invitation.role
        if registration_role == User.Role.RIDER:
            return render(request, rider_template_path, context)

        if registration_role == User.Role.VENDOR:
            return render(request, vendor_template_path, context)

    if request.method == 'POST':
        token = request.POST.get('token', '')
        invitation = get_object_or_404(Invitation, token=token)

        if not invitation.is_valid():
            return redirect('accounts:invalid_invite')

        registration_role = invitation.role if token else User.Role.CUSTOMER
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        errors = {}
        if not username: errors['username'] = 'Username is required'
        if not first_name: errors['first_name'] = 'First name is required'
        if not last_name: errors['last_name'] = 'Last name is required'
        if not phone_number: errors['phone_number'] = 'Phone number is required for verification and payouts'
        if not password: errors['password'] = 'Password is required'
        if not confirm_password: errors['confirm_password'] = 'Enter password again for confirmation'

        if password and confirm_password and password != confirm_password:
            errors['password'] = 'Passwords do not match'

        if errors:
            template_mapping = {
                User.Role.CUSTOMER: customer_template_path,
                User.Role.RIDER: rider_template_path,
                User.Role.VENDOR: vendor_template_path
            }

            return render(request, template_mapping[registration_role], {
                'errors': errors,
                'token': token,
                'data': request.POST
            })

        if registration_role == User.Role.CUSTOMER:
            user = _handle_customer_sign_up(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
                phone_number=phone_number,
            )

            login(request, user)
            return redirect(get_dashboard_url(user))

        if registration_role == User.Role.RIDER:
            ghana_card_number = request.POST.get('ghana_card_number', '')
            ghana_card_image = request.POST.get('ghana_card_image', '')
            profile_image = request.POST.get('profile_image', '')
            student_id_number = request.POST.get('student_id_number', '')
            is_student = request.POST.get('is_student', False) == 'on'
            vehicle_type = request.POST.get('vehicle_type', '')
            date_of_birth = request.POST.get('date_of_birth', '')

            ghana_card_number_is_valid = validate_ghana_card(ghana_card_number)
            if not ghana_card_number_is_valid: errors['ghana_card_number'] = 'Invalid Ghana Card Number format'
            if not ghana_card_image: errors['ghana_card_image'] = 'Image of Ghana card is required for verification'
            if not profile_image: errors['profile_image'] = 'Selfie of yourself is required for verification'
            if is_student and not student_id_number: errors['student_id_number']
            if not vehicle_type: errors['vehicle_type'] = 'Please select type of vehicle'
            if not date_of_birth: errors['date_of_birth'] = 'Date of birth is required'


            if errors:
                template_mapping = {
                    User.Role.CUSTOMER: customer_template_path,
                    User.Role.RIDER: rider_template_path,
                    User.Role.VENDOR: vendor_template_path
                }
    
                return render(request, template_mapping[registration_role], {
                    'errors': errors,
                    'token': token,
                    'data': request.POST
                })

            user, rider_profile = _handle_rider_sign_up(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number
            )

    