from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from users.services.email_service import EmailService
from users.services.passcode_service import PasscodeService
from users.repositories.passcode_repository import PasscodeRepository
from users.models import Passcode
from utils.email_sender import EmailSender
from utils import setup_logger

logger = setup_logger(__name__)

class PasscodeView(APIView):
    permission_classes = (IsAuthenticated,)
    passcode_repository = PasscodeRepository(Passcode)
    passcode_service = PasscodeService(passcode_repository)
    email_service = EmailService(EmailSender())
    
    def get(self, request):
        try:
            if (request.user.is_verified):
                logger.info(f'User {request.user.email} already verified')
                return Response({
                    'message': 'User email already verified',
                    'status': True,
                    'data': {
                        'is_verified': True,
                    }
                }, status=status.HTTP_200_OK)
            
            passcode = self.passcode_service.generate_passcode()
            self.email_service.send_passcode_email(request.user, passcode)
            self.passcode_service.create_passcode({
                'user': request.user,
                'passcode': passcode
            })
            logger.info(
                f'Passcode generated and sent to user {request.user.email}'
            )
            response = Response({
                'message': 'OTP sent successfully',
                'status': True,
                'data': {
                    'is_verified': False,
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
        except Exception as e:
            logger.error(f'Error generating or sending passcode: {e}')
            return Response({
                'message': 'Failed to send OTP',
                'status': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)