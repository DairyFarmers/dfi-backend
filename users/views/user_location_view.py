from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models.user_location import UserLocation
from users.serializers.user_settings_serializer import UserLocationSerializer
from exceptions import ServiceException
from utils import setup_logger

logger = setup_logger(__name__)

class UserLocationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's locations"""
        try:
            locations = UserLocation.objects.filter(
                user=request.user,
                is_active=True
            ).order_by('-is_primary', '-created_at')
            location_data = UserLocationSerializer(locations, many=True).data

            return Response({
                "status": True,
                "message": "Locations retrieved successfully",
                "data": location_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving locations: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Create new location"""
        try:
            request.data['user'] = request.user.id
            serializer = UserLocationSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({
                    "status": True,
                    "message": "Location created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                "status": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error creating location: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """Update location information"""
        try:
            location_id = request.data.get('locationId')
            if not location_id:
                raise ServiceException("Location ID is required")
            
            location = get_object_or_404(
                UserLocation,
                id=location_id,
                user=request.user
            )
            
            if 'is_primary' in request.data and request.data['is_primary']:
                # Set all other locations to non-primary
                UserLocation.objects.filter(
                    user=request.user,
                    is_primary=True
                ).update(is_primary=False)
                location.is_primary = True
            
            serializer = UserLocationSerializer(
                location,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                updated_locations = UserLocation.objects.filter(
                    user=request.user,
                    is_active=True
                ).order_by('-is_primary', '-created_at')
                locations_data = UserLocationSerializer(updated_locations, many=True).data
                
                return Response({
                    "status": True,
                    "message": "Location updated successfully",
                    "data": locations_data
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except ServiceException as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating location: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, location_id=None):
        """Delete a location"""
        try:
            if not location_id:
                raise ServiceException("Location ID is required")

            location = get_object_or_404(
                UserLocation,
                id=location_id,
                user=request.user
            )
            
            location.is_active = False
            location.save()

            return Response({
                "status": True,
                "message": "Location deleted successfully"
            }, status=status.HTTP_200_OK)

        except ServiceException as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error deleting location: {str(e)}")
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)