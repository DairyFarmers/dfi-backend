from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from users.services import B2BUserService
from users.serializers.b2buser_serializer import B2BUserSerializer

class B2BApprovalView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        service = B2BUserService()
        user = service.approve_user(user_id)
        if user:
            return Response(
                B2BUserSerializer(user).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )