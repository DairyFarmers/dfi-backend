from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Max, Count
from chats.models.chat import Message
from chats.serializers.chat_serializers import MessageSerializer, ChatPreviewSerializer
from users.models.user import User
from chats.serializers.chat_serializers import UserSerializer
from utils import setup_logger

logger = setup_logger(__name__)

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).order_by('timestamp')

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get chat history with a specific user"""
        logger.info(f"Fetching chat history with user ID: {pk}")
        messages = Message.objects.filter(
            Q(sender=request.user, receiver_id=pk) |
            Q(sender_id=pk, receiver=request.user)
        ).order_by('timestamp')
        
        # Mark messages as read
        messages.filter(receiver=request.user, is_read=False).update(is_read=True)
        logger.info(f"Marked {messages.filter(receiver=request.user, is_read=False).count()} messages as read")
        
        serializer = self.get_serializer(messages, many=True)
        return Response({
            'status': True,
            'message': 'Chat history retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def active_chats(self, request):
        """Get list of active chats with last message and unread count"""
        # Get users with whom the current user has chatted
        logger.info(f"Fetching active chats for user: {request.user.id}")
        chat_partners = User.objects.filter(
            Q(sent_messages__receiver=request.user) |
            Q(received_messages__sender=request.user)
        ).distinct()

        chats = []
        for partner in chat_partners:
            last_message = Message.objects.filter(
                Q(sender=request.user, receiver=partner) |
                Q(sender=partner, receiver=request.user)
            ).order_by('-timestamp').first()

            unread_count = Message.objects.filter(
                sender=partner,
                receiver=request.user,
                is_read=False
            ).count()

            if last_message:
                chats.append({
                    'user': partner,
                    'last_message': last_message.text,
                    'unread_count': unread_count,
                    'timestamp': last_message.timestamp
                })

        # Sort by latest message
        chats.sort(key=lambda x: x['timestamp'], reverse=True)
        logger.info(f"Found {len(chats)} active chats for user: {request.user.id}")
        serializer = ChatPreviewSerializer(chats, many=True)
        return Response({
            'status': True,
            'message': 'Active chats retrieved successfully',
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def search_users(self, request):
        """Search users by name or email"""
        query = request.query_params.get('q', '').strip()
        logger.info(f"Search query: {query}")
        
        if len(query) < 2:
            return Response([])

        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(
            id=request.user.id
        )[:10]  # Limit to 10 results
        
        logger.info(f"Found {users.count()} users for query: {query}")
        serializer = UserSerializer(users, many=True)
        return Response({
            'status': True,
            'message': 'Users found',
            'data': serializer.data
        })