import json
import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models.chat import Message
from users.models.user import User
from chats.serializers.chat_serializers import MessageSerializer
from chats.serializers.chat_serializers import UserSerializer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from utils import setup_logger

logger = setup_logger(__name__)

jwt_auth = JWTAuthentication()

@sync_to_async
def get_user_from_token(token):
    try:
        validated_token = jwt_auth.get_validated_token(token)
        user = jwt_auth.get_user(validated_token)
        return user
    except Exception:
        return None

class ChatConsumer(AsyncWebsocketConsumer):    
    async def connect(self):
        cookies = self.scope.get('cookies', {})
        access_token = cookies.get('accessToken')
        logger.info(f"Access token: {access_token}")
        
        if not access_token:
            await self.close(code=4001)
            return
        
        user = await get_user_from_token(access_token)
        logger.info(f"User from token: {user}")
                
        if user is None:
            await self.close(code=4001)
            return
        
        self.user = user
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        
        if not self.receiver_id:
            await self.close(code=4001)
            return
        
        logger.info(f"User {self.user.id} connecting to chat with {self.receiver_id}")
        
        user_ids = sorted([str(self.user.id), self.receiver_id])
        self.room_name = f"chat_{'_'.join(user_ids)}"
        self.room_group_name = f"chat_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        logger.info(f"User {self.user.id} joined chat room {self.room_group_name}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            logger.info(f"Received data: {data}")
        
            if data.get('type') == 'chat_message':
                receiver_id = data.get('receiver_id')
                message = data.get('text', '')
                
                if message and receiver_id:
                    receiver = await self.get_user_by_id(receiver_id)
                    chat_message = await self.create_message(
                        sender=self.user,
                        receiver=receiver,
                        text=message
                    )
                    
                    chat_room = f"chat_{min(str(self.user.id), receiver_id)}_{max(str(self.user.id), receiver_id)}"
                    message_data = await self.serialize_message(chat_message)
                    await self.channel_layer.group_send(
                        chat_room,
                        {
                            'type': 'chat.message',
                            'message': message_data
                        }
                    )
                    
                    logger.info(
                        f"Message sent from {self.user.id} to \
                            {receiver_id} in room {chat_room}"
                        )       
            else:
                logger.warning(
                    f"Received unknown message type: \
                        {data.get('type')}"
                    )
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            await self.send(text_data=json.dumps({
                'error': 'Failed to process message'
            }))
            
    async def chat_message(self, event):
        """
        Handler for chat.message type events
        """
        try:
            message = event['message']
            # Send message to WebSocket
            await self.send(text_data=json.dumps(message))
        except Exception as e:
            logger.error(f"Error in chat_message: {str(e)}")

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"User {self.user.id} left chat room {self.room_group_name}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)
    
    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data

    @database_sync_to_async
    def create_message(self, sender, receiver, text):
        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            text=text,
            is_read=False
        )
        
    async def chat_notification(self, event):
        """Handle chat notifications"""
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def get_unread_count(self, receiver, sender):
        return Message.objects.filter(
            sender=sender,
            receiver=receiver,
            is_read=False
        ).count()

    @database_sync_to_async
    def serialize_user(self, user):
        return UserSerializer(user).data