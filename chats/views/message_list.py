from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from chats.models.chat import Message
from chats.serializers.chat_serializers import MessageSerializer
from users.models.user import User

class MessageList(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        selected_user = User.objects.get(id=user_id)
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=selected_user)) |
            (Q(sender=selected_user) & Q(receiver=request.user))
        ).order_by('timestamp')
        return Response(MessageSerializer(messages, many=True).data)