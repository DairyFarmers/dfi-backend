from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models.user_role import UserRole

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_permissions(request):
    """
    Get all permissions for the current user, including inherited permissions
    """
    user = request.user
    if not user.role:
        return Response({
            'permissions': {},
            'role': None,
            'role_name': None
        })

    return Response({
        'permissions': user.role.get_all_permissions(),
        'role': str(user.role.id),
        'role_name': user.role.name
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_permissions(request):
    """
    Get all available permissions in the system grouped by role
    Requires admin permission
    """
    if not request.user.has_permission('can_manage_roles'):
        return Response({
            'error': 'Permission denied',
            'detail': 'Requires can_manage_roles permission'
        }, status=403)

    roles = UserRole.objects.all()
    permissions_by_role = {}
    
    for role in roles:
        permissions_by_role[role.name] = {
            'id': str(role.id),
            'description': role.description,
            'permissions': role.get_all_permissions(),
            'priority': role.priority,
            'parent_role': str(role.parent_role.id) if role.parent_role else None
        }

    return Response(permissions_by_role) 