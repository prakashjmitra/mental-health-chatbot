import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';

export interface Message {
  id?: number;
  sender: 'user' | 'bot';
  content: string;
  timestamp?: string;
  is_crisis_detected?: boolean;
}

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  messages?: Message[];
  message_count?: number;
  last_message?: any;
}

export interface ChatResponse {
  conversation_id: number;
  user_message: Message;
  bot_message: Message;
  resources: MentalHealthResource[];
}

export interface Message {
  id?: number;
  content: string;
  sender: 'user'|'bot';
  timestamp?: string;
  conversation_id?: number;
  is_crisis_detected?: boolean;
  confidence_score?: number;
}

export interface MentalHealthResource {
  id: number;
  title: string;
  description: string;
  resource_type: string;
  url?: string;
  phone_number?: string;
  is_crisis_resource: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://127.0.0.1:8001/api';
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  // Current conversation state
  private currentConversationSubject = new BehaviorSubject<Conversation | null>(null);
  public currentConversation$ = this.currentConversationSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Health check
  healthCheck(): Observable<any> {
    return this.http.get(`${this.baseUrl}/health/`);
  }

  // Conversation methods
  getConversations(): Observable<Conversation[]> {
    return this.http.get<Conversation[]>(`${this.baseUrl}/conversations/`);
  }

  getConversation(id: number): Observable<Conversation> {
    return this.http.get<Conversation>(`${this.baseUrl}/conversations/${id}/`);
  }

  createConversation(): Observable<Conversation> {
    return this.http.post<Conversation>(`${this.baseUrl}/conversations/`, {}, this.httpOptions);
  }

  // Chat methods
  sendMessage(message: string, conversationId?: number): Observable<ChatResponse> {
    const payload = {
      message: message,
      ...(conversationId && { conversation_id: conversationId })
    };
    
    return this.http.post<ChatResponse>(`${this.baseUrl}/chat/`, payload, this.httpOptions);
  }

  // Resource methods
  getResources(): Observable<MentalHealthResource[]> {
    return this.http.get<MentalHealthResource[]>(`${this.baseUrl}/resources/`);
  }

  // State management
  setCurrentConversation(conversation: Conversation | null): void {
    this.currentConversationSubject.next(conversation);
  }

  getCurrentConversation(): Conversation | null {
    return this.currentConversationSubject.value;
  }
}