import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models.chat import Message
from users.models.user import User
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
        else:
            self.room_name = self.get_room_name(self.user.id, self.receiver_id)
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('text')

        if text:
            # Save to database
            receiver = await self.get_user(self.receiver_id)
            message = await self.create_message(self.user, receiver, text)

            # Broadcast
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'sender_id': self.user.id,
                        'receiver_id': self.receiver_id,
                        'text': text,
                        'timestamp': str(message.timestamp),
                        'sender_username': self.user.username,
                    }
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @staticmethod
    def get_room_name(user1_id, user2_id):
        return f"chat_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def create_message(self, sender, receiver, text):
        return Message.objects.create(sender=sender, receiver=receiver, text=text)