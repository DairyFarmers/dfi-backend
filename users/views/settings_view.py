from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.models.user_settings import UserSettings
from users.repositories.settings_repository import UserSettingsRepository
from users.services.settings_service import UserSettingsService
from users.serializers.user_settings_serializer import UserSettingsSerializer
from exceptions.exceptions import ServiceException
from utils import setup_logger

logger = setup_logger(__name__)

class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = UserSettingsSerializer
    repository = UserSettingsRepository(UserSettings)
    service = UserSettingsService(repository)

    def get(self, request):
        """Get user settings"""
        try:
            settings = self.service.get_user_settings(
                request.user.id
            )
            
            if not settings:
                return Response({
                    "status": False,
                    "message": "Settings not found"
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer(
                settings, 
                context={'request': request}
            )
            return Response({
                "status": True,
                "message": "Settings retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except ServiceException as e:
            logger.error(f"Service error retrieving user settings: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error retrieving user settings: {str(e)}")
            return Response({
                "status": False,
                "message": "Failed to retrieve settings"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Update user settings",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'privacy_settings': openapi.Schema(
                    type=openapi.TYPE_OBJECT
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Settings updated successfully",
                schema=UserSettingsSerializer
            ),
            400: "Invalid data",
            404: "Settings not found",
            500: "Internal server error"
        }
    )
    def put(self, request):
        """Update user settings"""
        try:
            serializer = self.serializer(
                data=request.data,
                partial=True,
                context={'request': request}
            )
            
            if not serializer.is_valid():
                return Response({
                    "status": False,
                    "message": "Invalid data",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_settings = self.service.update_settings(
                request.user.id,
                serializer.validated_data
            )
            
            if not updated_settings:
                return Response({
                    "status": False,
                    "message": "Settings not found"
                }, status=status.HTTP_404_NOT_FOUND)

            response_serializer = self.serializer(
                updated_settings,
                context={'request': request}
            )
            return Response({
                "status": True,
                "message": "Settings updated successfully",
                "data": response_serializer.data
            }, status=status.HTTP_200_OK)
        except ServiceException as e:
            logger.error(f"Service error updating user settings: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating user settings: {str(e)}")
            return Response({
                "status": False,
                "message": "Failed to update settings"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)