from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_yasg.utils import swagger_auto_schema
from utils import setup_logger

logger = setup_logger(__name__)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout the user by blacklisting \
            the refresh token",
        responses={
            200: "Successfully logged out",
            500: "Internal server error"
        }
    )
    def post(self, request):
        """Logout the user by deleting the session"""
        try:
            cookies_header = request.headers.get('Cookie', '')
            cookies = dict(
                cookie.split('=', 1) 
                for cookie in cookies_header.split('; ') 
                if cookie
            )
            refresh_token = cookies.get('refreshToken')
            
            if not refresh_token:
                logger.warning(f"No refresh token found in cookies for user {request.user.id}")
                return Response({
                    "status": False,
                    "message": "Refresh token not found in cookies"
                }, status=status.HTTP_401_UNAUTHORIZED)

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(
                    f"Successfully blacklisted token for user {request.user.id}"
                )
                response = Response({
                    "status": True,
                    "message": "Successfully logged out"
                }, status=status.HTTP_200_OK)

                response.delete_cookie('accessToken', path='/')
                response.delete_cookie('refreshToken', path='/')
            except TokenError as e:
                logger.error(
                    f"Invalid refresh token for user {request.user.id}: {str(e)}"
                )
                return Response({
                    "status": False,
                    "message": "Invalid refresh token"
                }, status=status.HTTP_401_UNAUTHORIZED)

            logger.info(f"User {request.user.id} logged out successfully")
            return response

        except Exception as e:
            logger.error(f"Error logging out user {request.user.id}: {str(e)}")
            return Response({
                "status": False,
                "message": "An error occurred while logging out",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)