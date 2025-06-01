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

class UserRoleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRoleSerializer

    def check_admin_permission(self, user):
        if not user.has_permission('can_manage_roles'):
            logger.warning(f"User {user} attempted to access role management without permission")
            raise PermissionDenied("You don't have permission to manage roles")

    def get_role(self, role_id):
        try:
            return UserRole.objects.get(id=role_id)
        except UserRole.DoesNotExist:
            logger.warning(f"Attempted to access non-existent role with ID: {role_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving role with ID {role_id}: {str(e)}")
            return None

    @swagger_auto_schema(
        operation_description="Get a specific user role",
        responses={200: UserRoleSerializer()}
    )
    def get(self, request, role_id):
        try:
            logger.info(f"User {request.user} is retrieving role {role_id}")
            role = self.get_role(role_id)
            if not role:
                return Response({
                    'message': 'Role not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(role)
            return Response({
                'status': True,
                'message': 'Role fetched successfully',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"Error retrieving role {role_id}: {str(e)}")
            return Response({
                'message': 'Failed to retrieve role'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Update a user role",
        request_body=UserRoleSerializer,
        responses={200: UserRoleSerializer()}
    )
    def put(self, request, role_id):
        try:
            logger.info(f"User {request.user} is updating role {role_id}")
            self.check_admin_permission(request.user)
            
            role = self.get_role(role_id)
            if not role:
                return Response({
                    'message': 'Role not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(role, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Role {role_id} updated successfully")
                return Response({
                    'status': True,
                    'message': 'Role updated successfully',
                    'data': serializer.data
                })
            
            logger.warning(f"Invalid data for role update: {serializer.errors}")
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"Error updating role {role_id}: {str(e)}")
            return Response({
                'message': 'Failed to update role'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a user role",
        responses={204: "No content"}
    )
    def delete(self, request, role_id):
        try:
            logger.info(f"User {request.user} is deleting role {role_id}")
            self.check_admin_permission(request.user)
            
            role = self.get_role(role_id)
            if not role:
                return Response({
                    'message': 'Role not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            if role.users.exists():
                logger.warning(f"Attempted to delete role {role_id} with active users")
                return Response({
                    'message': 'Cannot delete role as it is assigned to users'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            role.delete()
            logger.info(f"Role {role_id} deleted successfully")
            return Response({
                'status': True,
                'message': 'Role deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"Error deleting role {role_id}: {str(e)}")
            return Response({
                'message': 'Failed to delete role'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)