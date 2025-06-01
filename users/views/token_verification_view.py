from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


class TokenVerificationView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            user = request.user
            
            # Get role data if it exists
            role_data = None
            if user.role:
                role_data = {
                    'id': str(user.role.id),
                    'name': user.role.name,
                    'permissions': user.role.get_all_permissions()
                }
                
            response = Response({
                'message': 'User authenticated successfully',
                'status': True,
                'data': {
                    'email': user.email,
                    'id': user.id,
                    'full_name': user.get_full_name,
                    'is_verified': user.is_verified,
                    'role': role_data,
                    'status': True,
                }}, status=status.HTTP_200_OK)
                
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'], 
                value=request.auth,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            return response
        except Exception as e:
            return Response({
                'message': 'Token verification failed',
                'status': False
            }, status=status.HTTP_400_BAD_REQUEST)