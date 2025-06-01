from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models.user_role import UserRole
from users.serializers.user_role_serializer import UserRoleSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from utils import setup_logger

logger = setup_logger(__name__)

class UserRoleView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRoleSerializer

    def check_admin_permission(self, user):
        if not user.has_permission('can_manage_roles'):
            logger.warning(f"User {user} attempted to access role management without permission")
            raise PermissionDenied("You don't have permission to manage roles")

    @swagger_auto_schema(
        operation_description="Get all user roles",
        responses={200: UserRoleSerializer(many=True)}
    )
    def get(self, request):
        try:
            logger.info(f"User {request.user} is retrieving all roles")
            roles = UserRole.objects.all()
            serializer = self.serializer_class(roles, many=True)
            return Response({
                'status': True,
                'message': 'User roles fetched successfully',
                'data': {
                    'results': serializer.data,
                    'count': roles.count()
                }
            })
        except Exception as e:
            logger.error(f"Error fetching roles: {str(e)}")
            return Response({
                'message': 'Failed to fetch roles'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Create a new user role",
        request_body=UserRoleSerializer,
        responses={201: UserRoleSerializer()}
    )
    def post(self, request):
        try:
            logger.info(f"User {request.user} is creating a new role")
            self.check_admin_permission(request.user)
            
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"New role created successfully: {serializer.data.get('name', '')}")
                return Response({
                    'status': True,
                    'message': 'Role created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            
            logger.warning(f"Invalid role data submitted: {serializer.errors}")
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"Error creating role: {str(e)}")
            return Response({
                'message': 'Failed to create role'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)