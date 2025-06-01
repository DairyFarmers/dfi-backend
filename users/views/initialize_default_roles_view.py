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

class InitializeDefaultRolesView(APIView):
    permission_classes = [IsAuthenticated]

    def check_admin_permission(self, user):
        if not user.has_permission('can_manage_roles'):
            logger.warning(f"User {user} attempted to access role management without permission")
            raise PermissionDenied("You don't have permission to manage roles")

    @swagger_auto_schema(
        operation_description="Initialize default user roles",
        responses={201: "Default roles created"}
    )
    def post(self, request):
        try:
            logger.info(f"{request.user} is initializing default roles")
            self.check_admin_permission(request.user)
            
            try:
                default_roles = UserRole.get_default_roles()
                created_roles = []

                for role_data in default_roles:
                    try:
                        role, created = UserRole.objects.get_or_create(
                            name=role_data['name'],
                            defaults={
                                'description': role_data['description'],
                                'permissions': role_data['permissions']
                            }
                        )
                        if created:
                            logger.info(f"Created new role: {role.name}")
                            created_roles.append(role.name)
                    except Exception as role_error:
                        logger.error(f"Error creating role {role_data['name']}: {str(role_error)}")
                        continue

                if created_roles:
                    logger.info(f"Successfully created {len(created_roles)} default roles")
                    return Response({
                        'status': True,
                        'message': f'Created default roles: {", ".join(created_roles)}',
                        'data': created_roles
                    }, status=status.HTTP_201_CREATED)
                
                logger.info("No new roles created - all default roles already exist")
                return Response({
                    'status': True,
                    'message': 'Default roles already exist',
                    'data': []
                }, status=status.HTTP_200_OK)

            except Exception as db_error:
                logger.error(f"Database error while creating roles: {str(db_error)}")
                return Response({
                    'message': 'Failed to create default roles'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except PermissionDenied as perm_error:
            logger.warning(f"Permission denied for user {request.user}: {str(perm_error)}")
            return Response({
                'message': str(perm_error)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"Unexpected error in role initialization: {str(e)}")
            return Response({
                'message': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)