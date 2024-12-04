from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from django.urls import reverse


class TokenVerificationViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            is_verified=True
        )

        # Generate an access token for the user
        self.token = str(AccessToken.for_user(self.user))

        # Define the URL
        self.url = reverse('token_verification')

    def test_successful_token_verification(self):
        # Authenticate the client with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        response = self.client.get(self.url)

        # Assertions for successful verification
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'])
        self.assertEqual(response.data['data']['email'], self.user.email)
        self.assertEqual(response.data['data']['id'], self.user.id)
        self.assertTrue(response.data['data']['is_verified'])

        # Check if the cookie is set
        auth_cookie = response.cookies.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        self.assertIsNotNone(auth_cookie)
        self.assertEqual(auth_cookie.value, self.token)
        self.assertTrue(auth_cookie['httponly'])
        self.assertEqual(auth_cookie['samesite'], settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'])

    def test_token_verification_without_authentication(self):
        response = self.client.get(self.url)

        # Assertions for unauthenticated request
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_token_verification_with_invalid_token(self):
        # Authenticate the client with an invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')

        response = self.client.get(self.url)

        # Assertions for invalid token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
