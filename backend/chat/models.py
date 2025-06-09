from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """Extended user profile for additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_in_crisis = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Conversation(models.Model):
    """Represents a chat conversation session"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class Message(models.Model):
    """Individual messages within a conversation"""
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=4, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_crisis_detected = models.BooleanField(default=False)
    confidence_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}..."

class MentalHealthResource(models.Model):
    """Mental health resources and coping strategies"""
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('exercise', 'Exercise'),
        ('hotline', 'Crisis Hotline'),
        ('app', 'Mobile App'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    keywords = models.CharField(max_length=500, help_text="Comma-separated keywords for matching")
    is_crisis_resource = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class ChatIntent(models.Model):
    """Stores recognized intents from user messages"""
    INTENT_TYPES = [
        ('greeting', 'Greeting'),
        ('anxiety', 'Anxiety'),
        ('depression', 'Depression'),
        ('stress', 'Stress'),
        ('crisis', 'Crisis'),
        ('coping', 'Coping Strategies'),
        ('general', 'General Support'),
    ]
    
    name = models.CharField(max_length=20, choices=INTENT_TYPES)
    keywords = models.TextField(help_text="Keywords that trigger this intent")
    response_template = models.TextField(help_text="Template response for this intent")
    
    def __str__(self):
        return f"Intent: {self.name}"