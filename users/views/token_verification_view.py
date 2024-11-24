from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

class TokenVerificationView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        response = Response({
            'message': 'User authenticated successfully',
            'status': True,
            'data': {
                'email': user.email,
                'id': user.id,
                'is_verified': user.is_verified,
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