from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from users.services.user_service import UserService
from exceptions.exceptions import ServiceException


class SignupViewTests(TestCase):
    def setUp(self):
        self.valid_user_data = {
            "email": "validuser@example.com",  # Must be a valid email address
            "first_name": "John",  # Minimum 1 character, max 100
            "last_name": "Doe",  # Minimum 1 character, max 100
            "password": "StrongPassword123!"  # Minimum 8 characters, max 128
        }

        self.invalid_user_data = {
            "email": "invalidemail",
            "first_name": "John",
            "last_name": "Doe",
            "password": "short"
        }

        self.url = reverse('signup')  # Replace 'signup' with the actual name of your URL pattern

    @patch('users.services.user_service.UserService.create_user')
    def test_post_valid_data(self, mock_create_user):
        """
        Test the SignupView POST method with valid user data.
        """
        mock_create_user.return_value = None  # Simulate successful user creation

        response = self.client.post(self.url, data=self.valid_user_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"message": "User account was created"})
        mock_create_user.assert_called_once_with(self.valid_user_data)

    def test_post_invalid_data(self):
        """
        Test the SignupView POST method with invalid user data.
        """
        response = self.client.post(self.url, data=self.invalid_user_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Invalid data, please check your input")

    @patch('users.services.user_service.UserService.create_user')
    def test_post_service_exception(self, mock_create_user):
        """
        Test the SignupView POST method when the service layer raises a ServiceException.
        """
        mock_create_user.side_effect = ServiceException("Service error")

        response = self.client.post(self.url, data=self.valid_user_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Error occured")
        mock_create_user.assert_called_once_with(self.valid_user_data)
