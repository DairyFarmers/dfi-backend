from rest_framework.views import APIView
from rest_framework.response import Response
from users.models.user import User
from rest_framework.response import Response

class UserList(APIView):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)  # Exclude yourself
        data = [{"id": user.id, "name": user.username, "role": user.role} for user in users]
        return Response(data)