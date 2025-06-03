from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models.user_contact import UserContact
from users.serializers.user_settings_serializer import UserContactSerializer
from utils import setup_logger

logger = setup_logger(__name__)

class UserContactView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's contact information"""
        try:
            contact = UserContact.objects.filter(user=request.user).first()
            contact_data = UserContactSerializer(contact).data if contact else None

            return Response({
                "status": True,
                "message": "Contact information retrieved successfully",
                "data": contact_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving contact info: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        """Update contact information"""
        try:
            contact, created = UserContact.objects.get_or_create(user=request.user)
            serializer = UserContactSerializer(
                contact,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Contact information updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error updating contact: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)