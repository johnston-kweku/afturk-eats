from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .decorators import role_required
from .models import Invitation, User
from .helpers import create_token
import json

# Create your views here.


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