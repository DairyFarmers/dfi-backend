from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import User
from users.repositories.user_repository import UserRepository
from users.services.email_service import EmailService
from unittest.mock import patch
from django.urls import reverse


class PasswordResetRequestViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            is_verified=True,
        )
        # API URL for the password reset request view
        self.url = reverse("password_reset_request")

    def test_password_reset_request_valid_data(self):
        """Test valid password reset request"""
        data = {
            'email': 'testuser@example.com',
        }

        # Make the POST request
        response = self.client.post(self.url, data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password reset requested')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    @patch.object(EmailService, 'send_password_reset_email')
    def test_password_reset_request_send_email_called(self, mock_send_email):
        """Test if the email sending method is called when a valid password reset request is made"""
        data = {
            'email': 'testuser@example.com',
        }

        # Make the POST request
        self.client.post(self.url, data)

        # Assert that the send_password_reset_email method was called
        mock_send_email.assert_called_once()

    def test_password_reset_request_invalid_data(self):
        """Test invalid data (missing email)"""
        data = {}

        # Make the POST request
        response = self.client.post(self.url, data)

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid data. Please check your input')

    def test_password_reset_request_user_not_found(self):
        """Test password reset request for non-existent user"""
        data = {
            'email': 'nonexistentuser@example.com',
        }

        # Make the POST request
        response = self.client.post(self.url, data)

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'User not found')
