from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
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
        # Define the URL for password reset request
        self.url = reverse("password_reset_request")  # Update with the correct endpoint name

    @patch('users.services.email_service.EmailService.send_password_reset_email')
    @patch('users.services.token_service.TokenService.generate_token')
    def test_password_reset_request_success(self, mock_generate_token, mock_send_email):
        # Mock the token generation and email sending
        mock_generate_token.return_value = "mock-token"
        mock_send_email.return_value = None  # Simulate email sending without actual email

        # Make the API request
        data = {
            "email": "testuser@example.com"
        }
        response = self.client.post(self.url, data)

        # Check the response status and message
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password reset requested')
        self.assertEqual(response.data['email'], self.user.email)

        # Verify that the token generation and email sending methods were called
        mock_generate_token.assert_called_once_with(self.user)
        mock_send_email.assert_called_once_with(self.user, "mock-token")

    @patch('users.services.email_service.EmailService.send_password_reset_email')
    @patch('users.services.token_service.TokenService.generate_token')
    def test_password_reset_request_invalid_email(self, mock_generate_token, mock_send_email):
        # Mock the token generation and email sending
        mock_generate_token.return_value = "mock-token"
        mock_send_email.return_value = None

        # Make the API request with an invalid email
        data = {
            "email": "nonexistentuser@example.com"
        }
        response = self.client.post(self.url, data)

        # Check that the response status is 400, since user doesn't exist
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'User not found')

        # Verify that token generation and email sending were not called
        mock_generate_token.assert_not_called()
        mock_send_email.assert_not_called()

    def test_password_reset_request_invalid_data(self):
        # Make the API request with invalid data (missing email)
        data = {}
        response = self.client.post(self.url, data)

        # Check that the response status is 400 for invalid data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid data. Please check your input')

