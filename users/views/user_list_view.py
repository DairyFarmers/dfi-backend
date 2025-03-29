from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from users.models.user import User
from users.repositories.user_repository import UserRepository
from users.services.user_service import UserService
from users.serializers.user_serializer import UserSerializer

class UserListView(APIView):
    serializer = UserSerializer
    repository = UserRepository(User)
    service = UserService(repository)

    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request):
        users = self.service.get_all_users()
        serializer = self.serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)