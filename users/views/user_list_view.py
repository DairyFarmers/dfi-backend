from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from users.models.user import User
from users.repositories.user_repository import UserRepository
from users.services.user_service import UserService
from users.serializers.user_serializer import UserSerializer
from django.core.paginator import Paginator

class UserListView(APIView):
    serializer = UserSerializer
    repository = UserRepository(User)
    service = UserService(repository)

    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request):
        try:
            users = self.service.get_all_users()
            serializer = self.serializer(users, many=True)
            fetch_all = request.query_params.get('fetch_all', 'false').lower() == 'true'

            if fetch_all:
                return Response({
                    'message': 'All users fetched successfully',
                    'status': True,
                    'data': {
                        'results': serializer.data,
                        'count': len(serializer.data)
                    }
                }, status=status.HTTP_200_OK)
            
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('size', 10)
            paginator = Paginator(users, page_size)
            current_page = paginator.get_page(page)
            serializer = self.serializer(current_page, many=True)
            return Response({
                'message': 'Users retrieved successfully',
                'status': True,
                'data': {
                    'results': serializer.data,
                    'count': paginator.count,
                    'num_pages': paginator.num_pages,
                    'next': current_page.number + 1 if current_page.has_next() else None,
                    'previous': current_page.number - 1 if current_page.has_previous() else None
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Failed to retrieve users'
            }, status=status.HTTP_400_BAD_REQUEST)