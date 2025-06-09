import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MentalHealthAI:
    def __init__(self):
        try:
            # Initialize sentiment analyzer
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            
            # Mental health keywords and patterns
            self.mental_health_keywords = {
                'anxiety': ['anxious', 'worried', 'nervous', 'panic', 'stress', 'tense', 'restless', 'overwhelmed'],
                'depression': ['depressed', 'sad', 'hopeless', 'empty', 'worthless', 'down', 'low', 'despair'],
                'crisis': ['suicide', 'kill myself', 'end it all', 'not worth living', 'hurt myself', 'die', 'harm myself'],
                'sleep': ['insomnia', 'sleep', 'tired', 'exhausted', 'fatigue', 'sleeping', 'rest'],
                'anger': ['angry', 'furious', 'rage', 'mad', 'irritated', 'frustrated', 'annoyed'],
                'positive': ['happy', 'good', 'great', 'excited', 'wonderful', 'amazing', 'fantastic'],
                'support': ['help', 'support', 'advice', 'guidance', 'assistance', 'therapy', 'counseling']
            }
            
            # Crisis phrases (more specific patterns)
            self.crisis_patterns = [
                r'\b(want to die|want to kill myself|kill myself|end my life|suicide|suicidal)\b',
                r'\b(hurt myself|harm myself|cut myself|not worth living)\b',
                r'\b(end it all|give up|can\'t go on|no point)\b'
            ]
            
            # Response templates organized by category and sentiment
            self.response_templates = {
                'anxiety': {
                    'high': [
                        "I understand you're feeling very anxious right now. Let's try some breathing exercises together. Take a deep breath in for 4 counts, hold for 4, and exhale for 6. Remember, this feeling will pass.",
                        "Anxiety can feel overwhelming, but you're not alone. Try grounding yourself by naming 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
                        "I hear that you're struggling with intense anxiety. It takes courage to reach out. Consider speaking with a mental health professional who can provide personalized coping strategies."
                    ],
                    'medium': [
                        "It sounds like you're experiencing some anxiety. That's completely normal, and there are ways to manage these feelings. Have you tried any relaxation techniques?",
                        "Anxiety is something many people face. Some helpful strategies include deep breathing, mindfulness, and regular exercise. What situations tend to trigger your anxiety?",
                        "I understand you're feeling anxious. Sometimes talking through what's bothering you can help. Would you like to share what's on your mind?"
                    ],
                    'low': [
                        "I notice you mentioned feeling a bit anxious. It's good that you're aware of your feelings. Sometimes just acknowledging anxiety can be the first step in managing it.",
                        "A little anxiety is normal, especially during stressful times. What helps you feel more calm and centered?"
                    ]
                },
                'depression': {
                    'high': [
                        "I'm really sorry you're going through such a difficult time. Depression can make everything feel hopeless, but there is help available. Please consider reaching out to a mental health professional.",
                        "What you're feeling sounds incredibly painful. Depression is a real illness, not a weakness. You deserve support and care. Have you been able to talk to anyone about how you're feeling?",
                        "I hear how much you're struggling. These feelings are valid, and you don't have to face them alone. Professional support can make a real difference in how you're feeling."
                    ],
                    'medium': [
                        "It sounds like you're going through a tough time. Depression affects many people, and it's important to know that it's treatable. Small steps, like maintaining a routine, can help.",
                        "I'm sorry you're feeling this way. Sometimes when we're depressed, everything feels harder. Have you been able to do any activities that usually bring you joy?",
                        "Depression can make even simple tasks feel overwhelming. Be gentle with yourself and consider seeking support from friends, family, or professionals."
                    ],
                    'low': [
                        "I notice you're feeling down. It's okay to have difficult days. Sometimes talking about what's bothering you can help lighten the load.",
                        "Everyone feels sad sometimes. If these feelings persist, it might help to talk to someone you trust or consider professional support."
                    ]
                },
                'crisis': [
                    "I'm very concerned about what you've shared. Your life has value, and there are people who want to help. Please reach out to a crisis helpline immediately: National Suicide Prevention Lifeline: 988.",
                    "What you're going through sounds incredibly painful, but please know that suicide is not the answer. There are people trained to help you through this. Please call 988 or go to your nearest emergency room.",
                    "I'm worried about your safety. These thoughts can feel overwhelming, but there is help available. Please contact the National Suicide Prevention Lifeline at 988 right now. You don't have to go through this alone."
                ],
                'positive': [
                    "I'm so glad to hear you're feeling good! It's wonderful when we can appreciate positive moments. What's been going well for you?",
                    "That's fantastic! It's great that you're in a positive space. How are you taking care of your mental health during good times?",
                    "I love hearing positive energy! Remember to savor these good feelings and maybe think about what's contributing to this positive mood."
                ],
                'general': [
                    "Thank you for sharing that with me. How are you feeling right now?",
                    "I'm here to listen and support you. Can you tell me more about what's on your mind?",
                    "It takes courage to reach out and talk about difficult feelings. What would be most helpful for you right now?",
                    "I appreciate you opening up. Mental health is just as important as physical health. How can I support you today?"
                ],
                'sleep': [
                    "Sleep issues can really affect our mental health. Good sleep hygiene includes going to bed at the same time, avoiding screens before bed, and creating a relaxing bedtime routine.",
                    "Trouble sleeping can be both a cause and symptom of stress or depression. Have you noticed any patterns in when you have difficulty sleeping?",
                    "Rest is so important for mental health. Some people find that meditation, reading, or gentle stretching before bed can help improve sleep quality."
                ],
                'support': [
                    "I'm glad you're looking for support - that's a positive step! While I can provide some guidance, speaking with a mental health professional can offer personalized help.",
                    "Seeking support shows strength, not weakness. There are many resources available including therapy, support groups, and crisis hotlines.",
                    "It's wonderful that you're reaching out. In addition to professional help, friends, family, and peer support groups can be valuable resources."
                ]
            }
            
            logger.info("Simplified MentalHealthAI initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing MentalHealthAI: {e}")
            # Fallback initialization
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            
    def analyze_message(self, message_text):
        """
        Comprehensive analysis of user message (without spaCy)
        """
        try:
            analysis = {
                'sentiment': self.get_sentiment(message_text),
                'entities': [],  # No spaCy, so empty entities
                'keywords': self.extract_keywords(message_text),
                'crisis_detected': self.detect_crisis(message_text),
                'category': self.categorize_message(message_text),
                'confidence': 0.0,
                'severity': 'low'
            }
            
            # Calculate confidence based on keyword matches and sentiment strength
            analysis['confidence'] = self.calculate_confidence(message_text, analysis)
            
            # Determine severity based on sentiment and keywords
            analysis['severity'] = self.determine_severity(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing message: {e}")
            return self.get_fallback_analysis()
    
    def get_sentiment(self, text):
        """Get sentiment analysis using VADER"""
        try:
            scores = self.sentiment_analyzer.polarity_scores(text)
            
            # Interpret compound score
            if scores['compound'] >= 0.05:
                sentiment_label = 'positive'
            elif scores['compound'] <= -0.05:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
                
            return {
                'compound': scores['compound'],
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu'],
                'label': sentiment_label
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 1, 'label': 'neutral'}
    
    def extract_keywords(self, text):
        """Extract mental health related keywords"""
        try:
            text_lower = text.lower()
            found_keywords = []
            
            for category, keywords in self.mental_health_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        found_keywords.append({
                            'keyword': keyword,
                            'category': category
                        })
            
            return found_keywords
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def detect_crisis(self, text):
        """Detect crisis situations using pattern matching"""
        try:
            text_lower = text.lower()
            
            for pattern in self.crisis_patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return True
                    
            return False
        except Exception as e:
            logger.error(f"Error in crisis detection: {e}")
            return False
    
    def categorize_message(self, text):
        """Categorize the message based on keywords"""
        try:
            text_lower = text.lower()
            category_scores = {}
            
            for category, keywords in self.mental_health_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    category_scores[category] = score
            
            if category_scores:
                return max(category_scores, key=category_scores.get)
            else:
                return 'general'
                
        except Exception as e:
            logger.error(f"Error categorizing message: {e}")
            return 'general'
    
    def calculate_confidence(self, text, analysis):
        """Calculate confidence score based on various factors"""
        try:
            confidence = 0.5  # Base confidence
            
            # Increase confidence based on keyword matches
            if analysis['keywords']:
                confidence += min(len(analysis['keywords']) * 0.1, 0.3)
            
            # Adjust based on sentiment strength
            sentiment_strength = abs(analysis['sentiment']['compound'])
            confidence += sentiment_strength * 0.2
            
            # Crisis detection increases confidence
            if analysis['crisis_detected']:
                confidence = 0.95
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.5
    
    def determine_severity(self, analysis):
        """Determine severity level based on analysis"""
        try:
            if analysis['crisis_detected']:
                return 'high'
            
            sentiment_compound = analysis['sentiment']['compound']
            
            if sentiment_compound <= -0.6:
                return 'high'
            elif sentiment_compound <= -0.3:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            logger.error(f"Error determining severity: {e}")
            return 'low'
    
    def generate_response(self, analysis, conversation_history=None):
        """Generate appropriate response based on analysis"""
        try:
            # Crisis response takes priority
            if analysis['crisis_detected']:
                return {
                    'content': random.choice(self.response_templates['crisis']),
                    'is_crisis_response': True,
                    'recommended_actions': ['contact_crisis_line', 'emergency_services']
                }
            
            # Get response based on category and severity
            category = analysis['category']
            severity = analysis['severity']
            
            if category in self.response_templates and isinstance(self.response_templates[category], dict):
                # Category has severity-based responses
                if severity in self.response_templates[category]:
                    response_options = self.response_templates[category][severity]
                else:
                    response_options = self.response_templates[category]['medium']
            elif category in self.response_templates:
                # Category has simple list of responses
                response_options = self.response_templates[category]
            else:
                # Default to general responses
                response_options = self.response_templates['general']
            
            response_content = random.choice(response_options)
            
            return {
                'content': response_content,
                'is_crisis_response': False,
                'recommended_actions': self.get_recommended_actions(analysis)
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'content': "I'm here to listen and support you. Can you tell me more about how you're feeling?",
                'is_crisis_response': False,
                'recommended_actions': []
            }
    
    def get_recommended_actions(self, analysis):
        """Get recommended actions based on analysis"""
        actions = []
        
        if analysis['crisis_detected']:
            actions.extend(['contact_crisis_line', 'emergency_services'])
        elif analysis['severity'] == 'high':
            actions.extend(['seek_professional_help', 'contact_support'])
        elif analysis['category'] in ['anxiety', 'depression']:
            actions.extend(['breathing_exercise', 'mindfulness', 'self_care'])
        elif analysis['category'] == 'sleep':
            actions.extend(['sleep_hygiene', 'relaxation'])
        
        return actions
    
    def get_fallback_analysis(self):
        """Fallback analysis when errors occur"""
        return {
            'sentiment': {'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 1, 'label': 'neutral'},
            'entities': [],
            'keywords': [],
            'crisis_detected': False,
            'category': 'general',
            'confidence': 0.3,
            'severity': 'low'
        }

# Initialize the AI service
mental_health_ai = MentalHealthAI()