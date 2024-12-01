from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from users.models import User
from users.services.login_service import LoginService
from exceptions.exceptions import ServiceException
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request


class LoginViewTests(TestCase):
    def setUp(self):
        self.url = '/api/v1/users/login'  # Your login URL
        self.valid_login_data = {
            "email": "validuser@example.com",
            "password": "StrongPassword123!"
        }

        self.invalid_user_data = {
            "email": "validuserexample.com",
            "password": "StrongPassword123!"
        }

        self.invalid_email_data = {
            "email": "invalidemail",  # Invalid email format
            "password": "StrongPassword123!"
        }

        self.invalid_password_data = {
            "email": "validuser@example.com",
            "password": ""  # Invalid password (empty)
        }

        self.invalid_email_length_data = {
            "email": 't' * 256,  # Invalid email (too long)
            "password": "StrongPassword123!"
        }

        self.url = reverse('login')  # Replace 'login' with the actual name of your URL pattern

    @patch('users.services.login_service.LoginService.login_user')
    def test_login_successful(self, mock_login_user):
        """
        Test the LoginView POST method with valid login data.
        """
        mock_login_user.return_value = {
            'email': 'validuser@example.com',
            'id': 1,
            'full_name': 'John Doe',
            'is_verified': True,
            'access_token': 'mock_access_token',
            'refresh_token': 'mock_refresh_token'
        }

        # Perform the POST request with the valid login data using self.client
        response = self.client.post(self.url, data=self.valid_login_data, content_type='application/json')

        # Check the response status and message
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'User authenticated successfully')

        # Create the expected arguments to match the email and password
        expected_args = (
            self.valid_login_data['email'],
            self.valid_login_data['password']
        )

        # Assert that the mock was called once with the expected email and password
        actual_args = mock_login_user.call_args[0][1:]  # Skip the first argument (request) in the actual call

        # Compare only the email and password
        self.assertEqual(expected_args, tuple(actual_args))

    def test_post_invalid_data(self):
        """
        Test the SignupView POST method with invalid user data.
        """
        response = self.client.post(self.url, data=self.invalid_user_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Invalid data. Please check your input")

    def test_login_invalid_email(self):
        """
        Test the LoginView POST method with invalid email format.
        """
        # Simulating an invalid email format scenario

        # Perform the POST request with invalid email data
        response = self.client.post(self.url, data=self.invalid_email_data, content_type='application/json')

        # Check the response status and message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid data. Please check your input')

    def test_login_invalid_password(self):
        """
        Test the LoginView POST method with empty password.
        """
        response = self.client.post(self.url, data=self.invalid_password_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid data. Please check your input')

    def test_login_invalid_email_length(self):
        """
        Test the LoginView POST method with email exceeding max length.
        """
        response = self.client.post(self.url, data=self.invalid_email_length_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid data. Please check your input')

    @patch('users.services.login_service.LoginService.login_user')
    def test_login_service_exception(self, mock_login_user):
        """
        Test the LoginView POST method when the service layer raises a ServiceException.
        """
        # Simulating the exception being raised
        mock_login_user.side_effect = ServiceException("Service error")

        # Perform the POST request using self.client.post
        response = self.client.post(self.url, data=self.valid_login_data, content_type='application/json')

        # Check the response status and message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid email or password. Please try again!')

        # Expected arguments (email and password)
        expected_args = (
            self.valid_login_data['email'],
            self.valid_login_data['password']
        )

        # Get the arguments passed to the mock (skipping the first argument, which is the request)
        actual_args = mock_login_user.call_args[0][1:]  # Skip the first argument (request)

        # Compare only the email and password, ignore the request argument
        self.assertEqual(expected_args, tuple(actual_args))

