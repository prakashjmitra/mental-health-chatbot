from django.contrib import admin
from .models import UserProfile, Conversation, Message, MentalHealthResource, ChatIntent

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'created_at', 'is_in_crisis']
    list_filter = ['is_in_crisis', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'title']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'content_preview', 'timestamp', 'is_crisis_detected']
    list_filter = ['sender', 'is_crisis_detected', 'timestamp']
    search_fields = ['content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(MentalHealthResource)
class MentalHealthResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'is_crisis_resource', 'created_at']
    list_filter = ['resource_type', 'is_crisis_resource', 'created_at']
    search_fields = ['title', 'description', 'keywords']

@admin.register(ChatIntent)
class ChatIntentAdmin(admin.ModelAdmin):
    list_display = ['name', 'keywords_preview']
    list_filter = ['name']
    
    def keywords_preview(self, obj):
        return obj.keywords[:100] + '...' if len(obj.keywords) > 100 else obj.keywords
    keywords_preview.short_description = 'Keywords'