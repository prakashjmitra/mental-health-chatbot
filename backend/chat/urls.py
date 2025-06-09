from django.urls import path
from .views import health_check, ConversationListView, ConversationDetailView, send_message, MentalHealthResourceListView, analyze_sentiment

urlpatterns = [
    # Health check
    path('health/', health_check, name='health_check'),
    
    # Conversations
    path('conversations/', ConversationListView.as_view(), name='conversation_list'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation_detail'),
    
    # Chat functionality  
    path('chat/', send_message, name='send_message'),
    
    # Resources
    path('resources/', MentalHealthResourceListView.as_view(), name='resource_list'),
    
    # AI Analysis
    path('analyze-sentiment/', analyze_sentiment, name='analyze_sentiment'),
]