from django.test import TestCase
from .models import User, Invitation
from django.urls import reverse
import json

# Create your tests here.

class InvitationTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_user',
            password='password123',
            phone_number='0505504257',
            role=User.Role.ADMIN,   
        )
        self.client.login(
            username='admin_user',
            password='password123'
        )


    def test_invitation_link(self):
        response = self.client.post(
            reverse('accounts:generate_invite_link'),
            data=json.dumps({'role': User.Role.RIDER}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Invitation.objects.count(), 1)