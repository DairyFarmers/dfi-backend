from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers.user_detail_serializer import UserDetailSerializer
from utils import setup_logger

logger = setup_logger(__name__)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        """Get user details by ID"""
        try:
            logger.info(f"User {request.user} is fetching details for user {user_id}")
            user = get_object_or_404(User, id=user_id)
            
            serializer = UserDetailSerializer(user)
            return Response({
                'status': True,
                'message': 'User details fetched successfully',
                'data': serializer.data
            })
        except User.DoesNotExist:
            logger.error(f"User with ID {user_id} not found")
            return Response({
                'status': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching user details: {str(e)}")
            return Response({
                'status': False,
                'message': 'Failed to fetch user details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, user_id):
        """Update user details"""
        try:
            logger.info(f"User {request.user} is updating user {user_id}")
            user = get_object_or_404(User, id=user_id)
            
            serializer = UserDetailSerializer(
                user, 
                data=request.data, 
                partial=True
            )
            if not serializer.is_valid():
                logger.error(f"Validation error: {serializer.errors}")
                return Response({
                    'status': False,
                    'message': 'Invalid data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'status': True,
                'message': 'User updated successfully',
                'data': serializer.data
            })
        except User.DoesNotExist:
            logger.error(f"User with ID {user_id} not found")
            return Response({
                'status': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return Response({
                'status': False,
                'message': 'Failed to update user'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self, request, user_id):
        """Delete user by ID"""
        try:
            logger.info(f"User {request.user} is deleting user {user_id}")
            user = get_object_or_404(User, id=user_id)
            
            if not self.can_delete_user(user):
                return Response({
                    'status': False,
                    'message': 'Cannot delete user with active dependencies'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.delete()
            return Response({
                'status': True,
                'message': 'User deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            logger.error(f"User with ID {user_id} not found")
            return Response({
                'status': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return Response({
                'status': False,
                'message': 'Failed to delete user'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)