from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_home(request):
    import logging
    logger = logging.getLogger(__name__)
    logger.info("ROOT URL ACCESSED!")
    print("ROOT URL HIT - this should appear in logs")
    
    return JsonResponse({
        'message': 'Mental Health Chatbot API - ROOT WORKING!',
        'status': 'running',
        'version': '1.0',
        'endpoints': {
            'health_check': '/api/health/',
            'conversations': '/api/conversations/',
            'chat': '/api/chat/',
            'resources': '/api/resources/',
            'sentiment_analysis': '/api/analyze-sentiment/',
            'admin': '/admin/'
        }
    })
urlpatterns = [
    path('', api_home, name='api_home'),  # Add this line for root URL
    path('api/', include('chat.urls')),
    path('admin/', admin.site.urls),
]