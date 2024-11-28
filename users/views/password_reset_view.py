from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers.password_reset_serializer import PasswordResetSerializer
from users.services.user_service import UserService
from users.services.token_service import TokenService
from users.repositories.user_repository import UserRepository
from users.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from exceptions.exceptions import ServiceException
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

class PasswordResetView(APIView):
    serializer = PasswordResetSerializer
    user_repository = UserRepository(User)
    user_service = UserService(user_repository)
    token_service = TokenService(PasswordResetTokenGenerator())

    @swagger_auto_schema(
        request_body=serializer,
        responses={200: 'Password changed', 400: 'Invalid Data'}
    )
    
    def post(self, request):
        serializer = self.serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "message": 'Invalid data. Please check your input'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = self.user_service.get_user_by_id(
                serializer.validated_data['user_id']
            )
            self.token_service.validate_token(
                user, 
                serializer.validated_data['token']
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({
                "message": "Password has been reset successfully"
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                "message": 'Invalid user ID'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ServiceException as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)