from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from ..models import MenuItem


class VendorActionTest(TestCase):
    def setUp(self):
        vendor_kofi = User.objects.create_user(
            username='vendor_kofi',
            password='password',
            phone_number='0200000000',
            role=User.Role.VENDOR,
            first_name='vendor',
            last_name='kofi'
        )

        vendor_kwame = User.objects.create_user(
            username='vendor_kwame',
            password='password',
            phone_number='0200000001',
            role=User.Role.VENDOR,
            first_name='vendor',
            last_name='kwame'
        )

    def test_add_menu_item(self):
        self.client.login(
            username='vendor_kofi',
            password='password'
        )
        self.client.post(reverse('vendor:add_menu_item'), )