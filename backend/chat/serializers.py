from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Conversation, Message, MentalHealthResource, ChatIntent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'age', 'created_at', 'is_in_crisis']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'is_crisis_detected']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'title', 'created_at', 'updated_at', 'is_active', 'messages']

class ConversationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for conversation lists"""
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'is_active', 'message_count', 'last_message']
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return {
                'content': last_message.content[:100] + '...' if len(last_message.content) > 100 else last_message.content,
                'sender': last_message.sender,
                'timestamp': last_message.timestamp
            }
        return None

class MentalHealthResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentalHealthResource
        fields = ['id', 'title', 'description', 'resource_type', 'url', 'phone_number', 'is_crisis_resource']

class ChatIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatIntent
        fields = ['id', 'name', 'keywords', 'response_template']

class ChatMessageInputSerializer(serializers.Serializer):
    """Serializer for incoming chat messages"""
    message = serializers.CharField(max_length=1000)
    conversation_id = serializers.IntegerField(required=False)