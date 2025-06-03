from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from users.models.user import User
from users.repositories.user_repository import UserRepository
from users.services.user_service import UserService
from users.serializers.user_serializer import UserSerializer
from utils import setup_logger

logger = setup_logger(__name__)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = UserSerializer
    repository = UserRepository(User)
    service = UserService(repository)
    
    @swagger_auto_schema(
        request_body=UserSerializer, 
        responses={200: "User Updated"}
    )
    def put(self, request):
        try:
            logger.info(f"Updating user with ID: {request.user.id}")
            user = self.service.get_user_by_id(request.user.id)
            serializer = self.serializer(
                user, 
                data=request.data, 
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f"User with ID: {request.user.id} updated successfully"
                )
                return Response({
                    "status": True,
                    "message": "User updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
                
            return Response({
                "status": False,
                "message": "Invalid data",
                "errors": serializer.errors    
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while updating the user",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        request_body=UserSerializer, 
        responses={200: "User Updated"}
    )
    def get(self, request):
        try:
            logger.info(f"Retrieving user with ID: {request.user.id}")
            user = self.service.get_user_by_id(request.user.id)
            serializer = self.serializer(user)
            return Response({
                "status": True,
                "message": "User retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while retrieving the user",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        request_body=UserSerializer, 
        responses={200: "User Deleted"}
    )
    def delete(self, request):
        try:
            logger.info(f"Deleting user with ID: {request.user.id}")
            user = self.service.get_user_by_id(request.user.id)
            
            if user:
                user.delete()
                logger.info(
                    f"User with ID: {request.user.id} deleted successfully"
                )
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            return Response({
                "status": False,
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while deleting the user",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)