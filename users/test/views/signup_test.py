import pytest
from unittest.mock import MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.serializers.signup_serializer import SignupSerializer
from users.models import User
from exceptions.exceptions import ServiceException
from users.services.user_service import UserService


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def valid_user_data():
    return {
        "email": "validuser@example.com",  # Must be a valid email address
        "first_name": "John",  # Minimum 1 character, max 100
        "last_name": "Doe",  # Minimum 1 character, max 100
        "password": "StrongPassword123!"  # Minimum 8 characters, max 128

    }


@pytest.fixture
def mock_user_service(mocker):
    return mocker.patch('users.services.user_service.UserService')


@pytest.fixture
def mock_user_service_create(mock_user_service):
    return mock_user_service.return_value.create_user


@pytest.fixture
def mock_user_service2(mocker):
    return mocker.patch('users.services.user_service.UserService')


@pytest.fixture
def mock_user_service_create2(mock_user_service2):
    return mock_user_service2.return_value.create_user


@pytest.mark.django_db
def test_post_valid_data(api_client, valid_user_data, mock_user_service_create):
    """
    Test the SignupView POST method with valid user data.
    """
    mock_user_service_create.return_value = None  # Simulate successful user creation

    url = reverse('signup')  # Replace 'signup' with the actual name of your URL pattern
    response = api_client.post(url, data=valid_user_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {"message": "User account was created"}
    mock_user_service_create.assert_called_once_with(valid_user_data)


@pytest.mark.django_db
def test_post_invalid_data(api_client):
    """
    Test the SignupView POST method with invalid user data.
    """
    invalid_user_data = {
        "email": "invalidemail",
        "first_name": "John",  # Minimum 1 character, max 100
        "last_name": "Doe",  # Minimum 1 character, max 100
        "password": "short"
    }

    url = reverse('signup')  # Replace 'signup' with the actual name of your URL pattern
    response = api_client.post(url, data=invalid_user_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "Invalid data, please check your input"


@pytest.mark.django_db
def test_post_service_exception(api_client, valid_user_data, mock_user_service_create):
    """
    Test the SignupView POST method when the service layer raises a ServiceException.
    """

    mock_user_service_create.side_effect = ServiceException("Service error")

    url = reverse('signup')  # Replace 'signup' with the actual name of your URL pattern
    response = api_client.post(url, data=valid_user_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "Error occured"
    mock_user_service_create.assert_called_once_with(valid_user_data)







