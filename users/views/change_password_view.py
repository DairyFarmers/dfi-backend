from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers.change_password_serializer import ChangePasswordSerializer
from users.services.user_service import UserService
from users.repositories.user_repository import UserRepository
from users.models import User
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from exceptions.exceptions import ServiceException
from utils import setup_logger

logger = setup_logger(__name__)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = ChangePasswordSerializer
    repository = UserRepository(User)
    user_service = UserService(repository)
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer(*args, **kwargs)
    
    @swagger_auto_schema(
        request_body=serializer,
        responses={200: 'Password changed', 400: 'Invalid Data'}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": False,
                "message": 'Invalid data. Please check your input'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = self.user_service.get_user_by_id(request.user.id)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                "status": True,
                "message": "Password has been changed successfully"
            }, status=status.HTTP_200_OK)
        except ServiceException as e:
            logger.error(f"Error changing password: {str(e)}")
            return Response({
                "status": False,
                "message": "Error changing password"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({
                "status": False,
                "message": "An unexpected error occurred. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)