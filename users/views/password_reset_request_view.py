from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers.password_reset_request_serializer import (
    PasswordResetRequestSerializer
)
from utils.email_sender import EmailSender
from users.repositories.user_repository import UserRepository
from users.models import User
from users.services.email_service import EmailService
from users.services.user_service import UserService
from users.services.token_service import TokenService
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from exceptions.exceptions import ServiceException
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

class PasswordResetRequestView(APIView):
    serializer = PasswordResetRequestSerializer
    user_repository = UserRepository(User)
    user_service = UserService(user_repository)
    token_service = TokenService(PasswordResetTokenGenerator())
    email_service = EmailService(EmailSender())

    @swagger_auto_schema(
        request_body=serializer,
        responses={200: 'Password reset requested', 400: 'Invalid Data'}
    )
    
    def post(self, request):
        serializer = self.serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(
                f'Invalid data for password reset request: {serializer.errors}'
            )
            return Response({
                "message": 'Invalid data. Please check your input'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:            
            user = self.user_service.get_user_by_email(
                serializer.validated_data['email']
            )
            token = self.token_service.generate_token(user)
            self.email_service.send_password_reset_email(user, token)
            logger.info(
                f'Password reset email sent to {user.email}'
            )
            return Response({
                'status': True,
                'message': 'Password reset requested',
            }, status=status.HTTP_200_OK)
        except ServiceException as e:
            logger.error(
                f'Error in password reset request: {str(e)}'
            )
            return Response({
                'status': True,
                'message': 'Password reset requested'
            }, status=status.HTTP_200_OK)
                    