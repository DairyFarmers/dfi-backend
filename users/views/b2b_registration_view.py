from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers.b2buser_registration_serializer import B2BUserRegistrationSerializer
from users.services import B2BUserService

class B2BRegistrationView(APIView):
    def post(self, request):
        serializer = B2BUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            service = B2BUserService()
            user = service.register_user(serializer.validated_data)
            return Response(
                B2BUserRegistrationSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)