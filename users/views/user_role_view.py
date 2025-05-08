from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models.user_role import UserRole
from users.serializers.user_role_serializer import UserRoleSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied

class UserRoleView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRoleSerializer

    def check_admin_permission(self, user):
        if not user.has_permission('can_manage_roles'):
            raise PermissionDenied("You don't have permission to manage roles")

    @swagger_auto_schema(
        operation_description="Get all user roles",
        responses={200: UserRoleSerializer(many=True)}
    )
    def get(self, request):
        roles = UserRole.objects.all()
        serializer = self.serializer_class(roles, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new user role",
        request_body=UserRoleSerializer,
        responses={201: UserRoleSerializer()}
    )
    def post(self, request):
        self.check_admin_permission(request.user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRoleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRoleSerializer

    def check_admin_permission(self, user):
        if not user.has_permission('can_manage_roles'):
            raise PermissionDenied("You don't have permission to manage roles")

    def get_role(self, role_id):
        try:
            return UserRole.objects.get(id=role_id)
        except UserRole.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific user role",
        responses={200: UserRoleSerializer()}
    )
    def get(self, request, role_id):
        role = self.get_role(role_id)
        if not role:
            return Response(
                {"error": "Role not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(role)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a user role",
        request_body=UserRoleSerializer,
        responses={200: UserRoleSerializer()}
    )
    def put(self, request, role_id):
        self.check_admin_permission(request.user)
        role = self.get_role(role_id)
        if not role:
            return Response(
                {"error": "Role not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a user role",
        responses={204: "No content"}
    )
    def delete(self, request, role_id):
        self.check_admin_permission(request.user)
        role = self.get_role(role_id)
        if not role:
            return Response(
                {"error": "Role not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        if role.users.exists():
            return Response(
                {"error": "Cannot delete role as it is assigned to users"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InitializeDefaultRolesView(APIView):
    permission_classes = [IsAuthenticated]

    def check_admin_permission(self, user):
        if not user.has_permission('can_manage_roles'):
            raise PermissionDenied("You don't have permission to manage roles")

    @swagger_auto_schema(
        operation_description="Initialize default user roles",
        responses={201: "Default roles created"}
    )
    def post(self, request):
        self.check_admin_permission(request.user)
        default_roles = UserRole.get_default_roles()
        created_roles = []

        for role_data in default_roles:
            role, created = UserRole.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'permissions': role_data['permissions']
                }
            )
            if created:
                created_roles.append(role.name)

        if created_roles:
            return Response(
                {"message": f"Created default roles: {', '.join(created_roles)}"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Default roles already exist"},
            status=status.HTTP_200_OK
        ) 