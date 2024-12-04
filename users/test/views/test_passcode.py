from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Passcode
from unittest.mock import patch
from django.urls import reverse
from django.conf import settings


class PasscodeViewTest(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            is_verified=False
        )

        # Authenticate the client with the test user
        self.client.force_authenticate(user=self.user)
        self.url = reverse('passcode')  # URL for the PasscodeView

    @patch('users.services.email_service.EmailService.send_passcode_email')
    @patch('users.services.passcode_service.PasscodeService.create_passcode')
    @patch('users.services.passcode_service.PasscodeService.generate_passcode')
    def test_passcode_sent_successfully(self, mock_generate_passcode, mock_create_passcode, mock_send_passcode_email):
        # Mocking the passcode generation to return a predefined value
        mock_passcode = '01949773'  # Simulate the auto-generated passcode
        mock_generate_passcode.return_value = mock_passcode  # Return the mocked passcode from the generator
        mock_create_passcode.return_value = mock_passcode  # Simulate passcode creation
        mock_send_passcode_email.return_value = None  # Simulate sending the email

        # Send GET request to OTP endpoint
        response = self.client.get(self.url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP sent successfully')
        self.assertTrue(response.data['status'])

        # Ensure that the passcode creation method was called once
        mock_create_passcode.assert_called_once_with({'user': self.user, 'passcode': mock_passcode})

        # Ensure that the send passcode email method was called once with the correct arguments
        mock_send_passcode_email.assert_called_once_with(self.user, mock_passcode)

    def test_passcode_not_authenticated(self):
        # Make request without authentication
        self.client.force_authenticate(user=None)  # Ensure user is unauthenticated
        response = self.client.get(self.url)

        # Check that it returns unauthorized error
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
