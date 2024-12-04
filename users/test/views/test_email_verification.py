from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Passcode
from django.utils import timezone
from unittest.mock import patch
from django.conf import settings
from django.urls import reverse


class EmailVerificationViewTest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            is_verified=False
        )
        self.client.force_authenticate(user=self.user)

        # Create a valid passcode with expiration time set to 60 minutes
        self.passcode = Passcode.objects.create(
            user=self.user,
            passcode="123456",
            created_at=timezone.now() - timezone.timedelta(minutes=15),  # Created 15 minutes ago
            expires_at=timezone.now() + timezone.timedelta(minutes=60)  # Expires in 60 minutes
        )

        # Use the name of the URL pattern defined in `urls.py`
        self.url = reverse("verification")  # Update with the correct name

    def test_email_verification_passcode_expired(self):
        # Simulate an expired passcode by setting the expires_at time to 60 minutes ago
        self.passcode.expires_at = timezone.now() - timezone.timedelta(minutes=60)  # 60 minutes ago
        self.passcode.save()

        with patch('users.services.passcode_service.PasscodeService.valid_passcode', return_value=False):
            # Simulate that the passcode is identified as expired
            response = self.client.post(self.url, data={"passcode": "12345"})  # Exact pass code is 123456

        # Assertions for expired passcode
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)  # Ensure a message is present in the response
        self.user.refresh_from_db()  # Refresh the user instance from the database
        self.assertFalse(self.user.is_verified)  # User should not be verified if the passcode is expired

    def test_email_verification_success(self):
        # Mock valid passcode service
        with patch('users.services.passcode_service.PasscodeService.valid_passcode', return_value=True):
            response = self.client.post(self.url, data={"passcode": "123456"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['data']['is_verified'])
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_email_verification_invalid_passcode(self):
        response = self.client.post(self.url, data={"passcode": "invalid_passcode"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_verified)

    def test_email_verification_missing_passcode(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_verified)
