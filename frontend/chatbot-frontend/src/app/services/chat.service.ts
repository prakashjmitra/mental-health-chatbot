import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface Message {
  id?: number;
  content: string;
  sender: 'user' | 'bot';
  timestamp?: string;
  conversation_id?: number;
  confidence_score?: number;
}

export interface MentalHealthResource {
  id: number;
  title: string;
  description: string;
  url: string;
  resource_type: string;
  phone_number?: string;  // Add optional phone_number field
}

export interface ChatResponse {
  conversation_id: number;
  user_message: Message;
  bot_message: Message;
  resources?: MentalHealthResource[];
  analysis?: {
    sentiment: {
      compound: number;
      positive: number;
      negative: number;
      neutral: number;
      label: string;
    };
    category: string;
    severity: string;
    keywords: Array<{
      keyword: string;
      category: string;
    }>;
    confidence: number;
    crisis_detected: boolean;
  };
  recommended_actions?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = environment.production 
    ? 'https://YOUR_BACKEND_URL/api' 
    : 'http://localhost:8001/api';

  constructor(private http: HttpClient) { }

  sendMessage(message: string, conversationId?: number): Observable<ChatResponse> {
    const body: any = { message };
    if (conversationId) {
      body.conversation_id = conversationId;
    }
    
    return this.http.post<ChatResponse>(`${this.apiUrl}/chat/`, body).pipe(
      tap(response => {
        // Store AI analysis for debugging
        if (response.analysis) {
          console.log('🧠 AI Analysis:', response.analysis);
          
          // Log interesting insights
          if (response.analysis.crisis_detected) {
            console.warn('⚠️ Crisis detected in message');
          }
          
          if (response.analysis.confidence > 0.8) {
            console.log('✅ High confidence AI response');
          }
          
          // Log sentiment details
          console.log(`😊 Sentiment: ${response.analysis.sentiment.label} (${(response.analysis.sentiment.compound * 100).toFixed(1)}%)`);
          console.log(`🏷️ Category: ${response.analysis.category} | Severity: ${response.analysis.severity}`);
          
          // Log detected keywords
          if (response.analysis.keywords.length > 0) {
            console.log('🔑 Keywords detected:', response.analysis.keywords.map(k => k.keyword).join(', '));
          }
        }
        
        // Update resources if provided
        if (response.resources && response.resources.length > 0) {
          console.log('📚 Resources provided:', response.resources.length);
        }
        
        // Log recommended actions
        if (response.recommended_actions && response.recommended_actions.length > 0) {
          console.log('💡 Recommended actions:', response.recommended_actions);
        }
      })
    );
  }

  getConversations(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/conversations/`);
  }

  getConversation(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/conversations/${id}/`);
  }

  createConversation(title?: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/conversations/`, { title });
  }

  getResources(): Observable<MentalHealthResource[]> {
    return this.http.get<MentalHealthResource[]>(`${this.apiUrl}/resources/`);
  }

  analyzeSentiment(text: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/analyze-sentiment/`, { message: text }).pipe(
      tap(response => {
        console.log('🔍 Standalone sentiment analysis:', response);
      })
    );
  }

  healthCheck(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/health/`).pipe(
      tap(response => {
        console.log('❤️ Health check:', response);
      })
    );
  }
}