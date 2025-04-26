# chat/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from chats.models.chat import Message
from chats.serializers.message_serializer import MessageSerializer
from users.models.user import User

class SendMessage(APIView):
    def get(self, request):
        data = request.data
        receiver = User.objects.get(id=data['receiver_id'])
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            text=data['text']
        )
        return Response(MessageSerializer(message).data)