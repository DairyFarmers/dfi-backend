from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers.registration_serializer import RegistrationSerializer
from users.services.user_service import UserService
from users.repositories.user_repository import UserRepository
from exceptions.exceptions import ServiceException
from users.models import User
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

class RegistrationView(APIView):
    serializer = RegistrationSerializer
    user_repository = UserRepository(User)
    user_service = UserService(user_repository)

    @swagger_auto_schema(
        request_body=serializer,
        responses={201: 'User account was created', 400: 'Invalid data'}
    )
    def post(self, request):
        serializer = self.serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            self.user_service.create_user(serializer.validated_data)
            return Response({
                "status": True,
                "message": "User account was created"
            }, status=status.HTTP_201_CREATED)
        except ServiceException as e:
            return Response({
                "status": False,
                "message": 'Error occured'
            }, status=status.HTTP_400_BAD_REQUEST)
            
