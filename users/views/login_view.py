from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers.login_serializer import LoginSerializer
from users.repositories.user_repository import UserRepository
from users.services.login_service import LoginService
from exceptions.exceptions import ServiceException
from users.models import User
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from utils import setup_logger

logger = setup_logger(__name__)

class LoginView(APIView):
    serializer = LoginSerializer
    user_repository = UserRepository(User)
    login_service = LoginService()

    @swagger_auto_schema(
        request_body=serializer,
        responses={200: 'User Logged In', 400: 'Invalid Data'}
    )
    
    def post(self, request):
        serializer = self.serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"Login failed: {serializer.errors}")
            return Response({
                "message": 'Invalid data. Please check your input'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user_data = self.login_service.login_user(
                request,
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            logger.info(f"User {user_data['email']} logged in successfully.")
            response = Response({
                'message': 'User authenticated successfully',
                'status': True,
                'data': {
                    'email': user_data['email'],
                    'id': user_data['id'],
                    'full_name': user_data['full_name'],
                    'is_verified': user_data['is_verified'],
                    'role': user_data['role'],
                }
            }, status=status.HTTP_200_OK)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'], 
                value=user_data['access_token'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'], 
                value=user_data['refresh_token'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            return response
        except ServiceException as e:
            logger.error(f"ServiceException during login: {str(e)}")
            return Response({
                "status": False,
                "message": "Invalid email or password. Please try again!"
            }, status=status.HTTP_400_BAD_REQUEST)