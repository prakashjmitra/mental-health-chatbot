from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import UserProfile, Conversation, Message, MentalHealthResource, ChatIntent
from .serializers import (
    ConversationSerializer, ConversationListSerializer, MessageSerializer,
    MentalHealthResourceSerializer, ChatMessageInputSerializer, UserProfileSerializer
)
from .ai_service import mental_health_ai  # Import our AI service
import random
import logging

logger = logging.getLogger(__name__)

class ConversationListView(generics.ListCreateAPIView):
    """List all conversations or create a new one"""
    serializer_class = ConversationListSerializer
    permission_classes = [AllowAny]  # Change this later for authentication
    
    def get_queryset(self):
        # For now, return all conversations. Later, filter by user
        return Conversation.objects.all()
    
    def perform_create(self, serializer):
        # For now, use the first user. Later, use authenticated user
        user = User.objects.first()
        if not user:
            # Create a default user for testing
            user = User.objects.create_user(username='testuser', password='testpass')
        serializer.save(user=user)

class ConversationDetailView(generics.RetrieveAPIView):
    """Get a specific conversation with all messages"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]

class MentalHealthResourceListView(generics.ListAPIView):
    """List mental health resources"""
    queryset = MentalHealthResource.objects.all()
    serializer_class = MentalHealthResourceSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def send_message(request):
    """Enhanced message handling with AI-powered responses"""
    serializer = ChatMessageInputSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    message_content = serializer.validated_data['message']
    conversation_id = serializer.validated_data.get('conversation_id')
    
    try:
        # Get or create conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
            # Create new conversation
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(username='testuser', password='testpass')
            conversation = Conversation.objects.create(
                user=user,
                title=f"Chat {message_content[:30]}..."
            )
        
        # Save user message
        user_message = Message.objects.create(
            conversation=conversation,
            sender='user',
            content=message_content
        )
        
        # AI Analysis of the message
        logger.info(f"Analyzing message: {message_content}")
        analysis = mental_health_ai.analyze_message(message_content)
        logger.info(f"Analysis result: {analysis}")
        
        # Get conversation history for context
        recent_messages = Message.objects.filter(
            conversation=conversation
        ).order_by('-timestamp')[:10]
        
        conversation_history = [
            {'content': msg.content, 'sender': msg.sender} 
            for msg in reversed(recent_messages)
        ]
        
        # Generate AI-powered response
        ai_response = mental_health_ai.generate_response(
            analysis, 
            conversation_history
        )
        
        # Save bot message with AI analysis data
        bot_message = Message.objects.create(
            conversation=conversation,
            sender='bot',
            content=ai_response['content'],
            confidence_score=analysis['confidence']
        )
        
        # Get relevant resources based on AI analysis
        resources = get_ai_relevant_resources(analysis)
        
        # Prepare enhanced response
        response_data = {
            'conversation_id': conversation.id,
            'user_message': MessageSerializer(user_message).data,
            'bot_message': MessageSerializer(bot_message).data,
            'analysis': {
                'sentiment': analysis['sentiment'],
                'category': analysis['category'],
                'severity': analysis['severity'],
                'keywords': analysis['keywords'],
                'confidence': analysis['confidence'],
                'crisis_detected': analysis['crisis_detected']
            },
            'resources': resources,
            'recommended_actions': ai_response.get('recommended_actions', [])
        }
        
        logger.info(f"AI-enhanced response generated for conversation {conversation.id}")
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        # Fallback to simple response if AI fails
        bot_response = generate_bot_response(message_content)
        bot_message = Message.objects.create(
            conversation=conversation,
            sender='bot',
            content=bot_response
        )
        
        return Response({
            'conversation_id': conversation.id,
            'user_message': MessageSerializer(user_message).data,
            'bot_message': MessageSerializer(bot_message).data,
            'resources': get_relevant_resources(message_content),
            'analysis': None,  # No AI analysis available
            'recommended_actions': []
        })

def get_ai_relevant_resources(analysis):
    """Get relevant mental health resources based on AI analysis"""
    try:
        resources = []
        category = analysis.get('category', 'general')
        severity = analysis.get('severity', 'low')
        
        # Get resources based on category
        if category == 'crisis':
            resources = MentalHealthResource.objects.filter(
                resource_type='hotline'
            )[:3]
        elif category in ['anxiety', 'depression']:
            resources = MentalHealthResource.objects.filter(
                keywords__icontains=category
            )[:3]
        elif category == 'sleep':
            resources = MentalHealthResource.objects.filter(
                keywords__icontains='sleep'
            )[:2]
        else:
            # General resources
            resources = MentalHealthResource.objects.filter(
                resource_type='general'
            )[:2]
        
        # If high severity, prioritize professional help resources
        if severity == 'high' and not analysis.get('crisis_detected'):
            professional_resources = MentalHealthResource.objects.filter(
                resource_type='therapy'
            )[:1]
            resources = list(professional_resources) + list(resources)[:2]
        
        return MentalHealthResourceSerializer(resources, many=True).data
        
    except Exception as e:
        logger.error(f"Error getting AI relevant resources: {e}")
        # Fallback to simple resource matching
        return get_relevant_resources("")

# Keep your original function as fallback
def generate_bot_response(user_message):
    """Simple bot response generation (fallback when AI fails)"""
    user_message_lower = user_message.lower()
    
    # Crisis detection
    crisis_keywords = ['suicide', 'kill myself', 'end it all', 'hurt myself', 'can\'t go on']
    if any(keyword in user_message_lower for keyword in crisis_keywords):
        return """I'm really concerned about what you're sharing and your health. Your life has value and always know that there are people who want to help. 
        
Please reach out to a crisis helpline immediately:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741

If you're not comfortable with that, would you like me to help you find local resources or someone to talk to right away?"""
    
    # Anxiety responses
    anxiety_keywords = ['anxious', 'worry', 'panic', 'nervous', 'stressed']
    if any(keyword in user_message_lower for keyword in anxiety_keywords):
        responses = [
            "It sounds like you're dealing with some anxiety right now. That can feel really overwhelming. One thing that might help you is taking slow, deep breaths. Would you like me to guide you through a breathing exercise?",
            "Anxiety can be really difficult to manage. Remember that these feelings are temporary and will pass. Have you tried any grounding techniques before?",
            "I hear that you're feeling anxious. It's completely normal to feel this way sometimes. What's one small thing you could do right now to take care of yourself?"
        ]
        return random.choice(responses)
    
    # Depression responses
    depression_keywords = ['depressed', 'sad', 'hopeless', 'empty', 'alone']
    if any(keyword in user_message_lower for keyword in depression_keywords):
        responses = [
            "I'm sorry you're feeling this way. Depression can make everything feel heavy and difficult. You're not alone in this, and it's brave of you to reach out.",
            "Those feelings sound really hard to carry. While I can't replace professional help, I'm here to listen and support you. Have you been able to talk to anyone else about how you're feeling?",
            "Thank you for sharing that with me. Depression can make it hard to see past the current moment, but there is hope and help available."
        ]
        return random.choice(responses)
    
    # General supportive responses
    general_responses = [
        "Thank you for sharing that with me. How are you feeling right now?",
        "I'm here to listen and support you. Can you tell me a bit more about what's on your mind?",
        "It sounds like you have a lot going on. What would be most helpful for you to talk about today?",
        "I appreciate you opening up. What's one thing that's been weighing on your mind lately?"
    ]
    
    return random.choice(general_responses)

def get_relevant_resources(message):
    """Get relevant mental health resources based on message content (fallback)"""
    # Simple keyword matching for now
    resources = []
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['anxious', 'anxiety', 'panic', 'worry']):
        resources = MentalHealthResource.objects.filter(keywords__icontains='anxiety')[:3]
    elif any(word in message_lower for word in ['depressed', 'depression', 'sad']):
        resources = MentalHealthResource.objects.filter(keywords__icontains='depression')[:3]
    else:
        resources = MentalHealthResource.objects.filter(resource_type='general')[:2]
    
    return MentalHealthResourceSerializer(resources, many=True).data

@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_sentiment(request):
    """Standalone AI sentiment analysis endpoint"""
    try:
        message = request.data.get('message', '')
        if not message:
            return Response(
                {'error': 'Message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        analysis = mental_health_ai.analyze_message(message)
        
        return Response({
            'message': message,
            'sentiment': analysis['sentiment'],
            'category': analysis['category'],
            'severity': analysis['severity'],
            'confidence': analysis['confidence'],
            'crisis_detected': analysis['crisis_detected'],
            'keywords': analysis['keywords']
        })
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        return Response(
            {'error': 'Failed to analyze sentiment'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Enhanced health check endpoint"""
    try:
        # Test AI service
        test_analysis = mental_health_ai.analyze_message("Hello, how are you?")
        ai_status = "healthy" if test_analysis else "error"
    except Exception as e:
        ai_status = f"error: {str(e)}"
    
    return Response({
        'status': 'healthy',
        'message': 'Mental Health Chatbot API is running',
        'ai_service': ai_status,
        'features': [
            'sentiment_analysis',
            'crisis_detection',
            'keyword_extraction',
            'intelligent_responses',
            'confidence_scoring'
        ]
    })