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
    _handle_vendor_sign_up,
    _handle_admin_sign_up,
    validate_ghana_card
)
import json

# Create your views here.



def home(request):
    return render(request, 'accounts/index.html')


@role_required(User.Role.ADMIN)
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


@role_required(User.Role.ADMIN)
def invite_link(request):
    return render(request, 'register/invitation.html')






def invalid_invite(request):
    return render(request, 'errors/invalid_invite.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')  

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        errors = {}
        if not username: errors['username'] = 'Please provide a username.'
        if not password: errors['password'] = 'Please enter your password'
        if errors:
            return render(request, 'accounts/login.html', {'username': username, 'errors': errors})

        user = authenticate(request, username=username, password=password)

        if user is None:
            errors['user_does_not_exist'] = 'This account does not exist'
            return render(request, 'accounts/login.html', {'username': username, 'errors': errors})

        if not user.is_active:
            errors['account_deactivated'] = 'This account has been deactivated. Please contact support'
            return render(request, 'accounts/login.html', {'username': username})

        login(request, user)

        # Role-based redirect
        if user.role == user.Role.RIDER:
            return redirect(get_dashboard_url(user))
        elif user.role == user.Role.VENDOR:
            return redirect(get_dashboard_url(user))
        elif user.role == user.Role.CUSTOMER:
            return redirect(get_dashboard_url(user))
        elif user.role == user.Role.ADMIN:
            return redirect(get_dashboard_url(user))

        return redirect('accounts:home')  # fallback

    return render(request, 'accounts/login.html', {'username': ''})



def logout_view(request):
    logout(request)
    return redirect('accounts:login')



def user_registration(request):

    customer_template_path = 'register/customer_registration.html'
    rider_template_path = 'register/rider_registration.html'
    vendor_template_path = 'register/vendor_registration.html'
    admin_registration = 'register/admin_registration.html'

    template_mapping = {
        User.Role.CUSTOMER: customer_template_path,
        User.Role.RIDER: rider_template_path,
        User.Role.VENDOR: vendor_template_path,
        User.Role.ADMIN: admin_registration
    }
    if request.method == 'GET':
        token = request.GET.get('token', '')
        if not token:
            return render(request, customer_template_path)

        invitation = get_object_or_404(Invitation, token=token)

        if not invitation.is_valid():
            return redirect('accounts:invalid_invite')

        context = {'token': token}
        registration_role = invitation.role
        return render(request, template_mapping[registration_role], context)

    if request.method == 'POST':
        token = request.POST.get('token', '')
        if token:
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
            errors['passwords_do_not_match'] = 'Passwords do not match'

        if User.objects.filter(phone_number=phone_number).exists():
            errors['phone_number'] = 'This phone number is already in use'

        if User.objects.filter(username=username).exists():
            errors['username'] = 'This username already exists.'

        if email and User.objects.filter(email=email).exists():
            errors['email'] = 'This email is alraedy in use.'
        
        if errors:
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
            ghana_card_image = request.FILES.get('ghana_card_image', '')
            profile_image = request.FILES.get('profile_image', '')
            student_id_number = request.POST.get('student_id_number', '')
            is_student = request.POST.get('is_student', False) == 'on'
            vehicle_type = request.POST.get('vehicle_type', '')
            date_of_birth = request.POST.get('date_of_birth', '')
            rented_vehicle = False
            if vehicle_type == 'REQUEST RENT':
                rented_vehicle = True

            ghana_card_number_is_valid = validate_ghana_card(ghana_card_number)

            if not ghana_card_number_is_valid: errors['ghana_card_number'] = 'Invalid Ghana Card Number format'
            if not ghana_card_image: errors['ghana_card_image'] = 'Image of Ghana card is required for verification'
            if not profile_image: errors['profile_image'] = 'Selfie of yourself is required for verification'
            if is_student and not student_id_number: errors['student_id_number'] = 'Student ID is required for riders who are also students.'
            if not vehicle_type: errors['vehicle_type'] = 'Please select type of vehicle'
            if not date_of_birth: errors['date_of_birth'] = 'Date of birth is required'


            if errors:
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
                phone_number=phone_number,
                ghana_card_image=ghana_card_image,
                ghana_card_number=ghana_card_number,
                date_of_birth=date_of_birth,
                vehicle_type=vehicle_type,
                is_student=is_student,
                student_id_number=student_id_number,
                rented_vehicle=rented_vehicle if rented_vehicle else False
            )
            invitation.is_used = True
            invitation.used_by = user
            invitation.save()
            return redirect('accounts:pending_approval')

        if registration_role == User.Role.VENDOR:
            ghana_card_number = request.POST.get('ghana_card_number', '')
            ghana_card_image = request.FILES.get('ghana_card_image', '')
            business_name = request.POST.get('business_name', '').strip()
            profile_image = request.FILES.get('profile_image', '')
            category = request.POST.get('category', '')
            date_of_birth = request.POST.get('date_of_birth', '')

            ghana_card_number_is_valid = validate_ghana_card(ghana_card_number)

            if not ghana_card_number_is_valid: errors['ghana_card_number'] = 'Invalid Ghana Card Number format.'
            if not business_name: errors['business_name'] = 'Business name is required.'
            if not profile_image: errors['profile_image'] = 'Selfie of yourself is required for verification.'
            if not category: errors['category'] = 'Please select at least one category'
            if not date_of_birth: errors['date_of_birth'] = 'Date of birth is required.'
            if not ghana_card_image: errors['ghana_card_image'] = 'Image of Ghana Card is required for verification.'


            if errors:
                return render(request, template_mapping[registration_role], {
                    'errors': errors,
                    'token': token,
                    'data': request.POST
                })

            user, vendor_profile = _handle_vendor_sign_up(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                business_name=business_name,
                category=category,
                date_of_birth=date_of_birth,
                ghana_card_image=ghana_card_image,
                ghana_card_number=ghana_card_number,
                profile_image=profile_image
            )
            invitation.is_used = True
            invitation.used_by = user
            invitation.save()

            return redirect('accounts:pending_approval')

        if registration_role == User.Role.ADMIN:
            user = _handle_admin_sign_up(
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                password=password
            )
            invitation.is_used = True
            invitation.used_by = user
            invitation.save()
            login(request, user)
            return redirect(get_dashboard_url(user))
        


def pending_approval(request):
    return render(request, 'register/pending_approval.html')