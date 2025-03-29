from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from users.models.user import User
from users.repositories.user_repository import UserRepository
from users.services.user_service import UserService
from users.serializers.user_serializer import UserSerializer

class UserView(APIView):
    serializer = UserSerializer
    repository = UserRepository(User)
    service = UserService(repository)
    
    @swagger_auto_schema(request_body=UserSerializer, responses={200: "User Updated"})
    def put(self, request, user_id):
        user = self.service.get_user_by_id(user_id)
        serializer = self.serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=UserSerializer, responses={200: "User Updated"})
    def get(self, request, user_id):
        user = self.service.get_user_by_id(user_id)
        serializer = self.serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=UserSerializer, responses={200: "User Deleted"})
    def delete(self, request, user_id):
        user = self.service.get_user_by_id(user_id)
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)