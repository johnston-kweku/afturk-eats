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

        self.rider = User.objects.create_user(
            username='rider',
            password='password123',
            phone_number='0595471021',
            role=User.Role.RIDER
        )

        self.client.login(
            username='admin_user',
            password='password123'
        )

        self.url = 'accounts:generate_invite_link'

    def test_invitation_link_creation(self):
        response = self.client.post(
            reverse(self.url),
            data=json.dumps({'role': User.Role.RIDER}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Invitation.objects.count(), 1)


    def test_invitation_invalid_json_structure(self):
        response = self.client.post(
            reverse(self.url),
            data={'role': 'ADMIN'}
        )
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid JSON structure.')
        self.assertEqual(Invitation.objects.count(), 0)

    def test_invitation_no_role(self):
        response = self.client.post(
            reverse(self.url),
            data=json.dumps({}),
            content_type='application/json'
        )
        data = response.json()
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Please provide a role.')
        self.assertEqual(Invitation.objects.count(), 0)


    def test_invitation__non_existent_role(self):
        response = self.client.post(
            reverse(self.url),
            data=json.dumps({
                'role': 'USER'
            }),
            content_type='application/json'
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Invalid role.')
        self.assertEqual(Invitation.objects.count(), 0)


    def test_invitation_unauthorised_user(self):
        self.client.logout()
        self.client.login(username='rider', password='password123')

        response = self.client.post(
            reverse(self.url),
            data=json.dumps({'role': 'ADMIN'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)  
        self.assertEqual(Invitation.objects.count(), 0)