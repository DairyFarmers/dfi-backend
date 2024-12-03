from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers.email_verification_serializer import (
    EmailVerificationSerializer
)
from users.services.user_service import UserService
from users.services.passcode_service import PasscodeService
from users.models import User
from users.models import Passcode
from users.repositories.user_repository import UserRepository
from users.repositories.passcode_repository import PasscodeRepository
from exceptions.exceptions import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from users.models import User, Passcode
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailVerificationView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = EmailVerificationSerializer
    user_repository = UserRepository(User)
    passcode_repository = PasscodeRepository(Passcode)
    user_service = UserService(user_repository)
    passcode_service = PasscodeService(passcode_repository)

    @swagger_auto_schema(
        request_body=serializer,
        responses={200: 'Email is verified', 400: 'Invalid Data'}
    )

    
    def post(self, request):
        serializer = self.serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "message": 'Invalid data. Please check your input'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            email_verified = self.user_service.is_email_verified(
                request.user.id
            )
            passcode = self.passcode_service.get_passcode(
                serializer.validated_data['passcode']
            )
            passcode_validated = self.passcode_service.valid_passcode(
                passcode,
            )
            self.user_service.update_user(
                request.user.id, 
                is_verified=passcode_validated
            )
            self.passcode_service.delete_passcode(
                passcode.passcode
            )
            response = Response({
                'message': 'User Email verified successfully!',
                'status': True,
                'data': {
                    'is_verified': True,
                }
            }, status=status.HTTP_200_OK)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'], 
                value=request.auth,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            return response
        except ServiceException as e:
            return Response({
                'message': 'Email verification failed',
            }, status=status.HTTP_400_BAD_REQUEST)