import { Component, OnInit, AfterViewChecked, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService, Message, MentalHealthResource } from '../../services/chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrls: ['./chat.css']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  // Expose Math to template
  Math = Math;

  messages: Message[] = [];
  resources: MentalHealthResource[] = [];
  currentMessage = '';
  isLoading = false;
  isTyping = false;
  showAIDebug = false;
  lastAnalysis: any = null;
  conversationId?: number;
  characterCount = 0;
  maxCharacters = 500;

  // Quick suggestion buttons
  quickSuggestions = [
    "I'm feeling anxious",
    "I need help with sleep",
    "I'm feeling down",
    "I need coping strategies"
  ];

  constructor(private chatService: ChatService) {}

  ngOnInit() {
    // Initialize with a welcome message
    this.messages = [{
      content: "Hello! I'm here to provide mental health support and resources. How are you feeling today?",
      sender: 'bot',
      timestamp: new Date().toISOString()
    }];

    // Load initial resources
    this.loadResources();
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  loadResources() {
    this.chatService.getResources().subscribe({
      next: (resources) => {
        this.resources = resources;
      },
      error: (error) => {
        console.error('Error loading resources:', error);
      }
    });
  }

  sendMessage() {
    if (this.currentMessage.trim()) {
      this.isLoading = true;
      this.isTyping = true;
      
      this.chatService.sendMessage(this.currentMessage, this.conversationId).subscribe({
        next: (response) => {
          this.messages.push(response.user_message);
          
          // Store AI analysis for debug panel
          if (response.analysis) {
            this.lastAnalysis = response.analysis;
          }
          
          // Add typing delay for bot response
          setTimeout(() => {
            this.messages.push(response.bot_message);
            if (response.resources) {
              this.resources = response.resources;
            }
            this.isLoading = false;
            this.isTyping = false;
            this.scrollToBottom();
          }, 1500);
          
          this.conversationId = response.conversation_id;
          this.currentMessage = '';
          this.characterCount = 0;
        },
        error: (error) => {
          console.error('Error sending message:', error);
          this.isLoading = false;
          this.isTyping = false;
          
          // Add error message
          this.messages.push({
            content: "I'm sorry, I encountered an error. Please try again.",
            sender: 'bot',
            timestamp: new Date().toISOString()
          });
        }
      });
    }
  }

  sendQuickSuggestion(suggestion: string) {
    this.currentMessage = suggestion;
    this.characterCount = suggestion.length;
    this.sendMessage();
  }

  onMessageInput() {
    this.characterCount = this.currentMessage.length;
  }

  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  scrollToBottom() {
    try {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      console.error('Error scrolling to bottom:', err);
    }
  }

  newChat() {
    // Clear current conversation
    this.messages = [{
      content: "Hello! I'm here to provide mental health support and resources. How are you feeling today?",
      sender: 'bot',
      timestamp: new Date().toISOString()
    }];
    this.conversationId = undefined;
    this.lastAnalysis = null;
    this.currentMessage = '';
    this.characterCount = 0;
    
    // Optionally create a new conversation on the backend
    this.chatService.createConversation().subscribe({
      next: (conversation) => {
        this.conversationId = conversation.id;
        console.log('New conversation created:', conversation.id);
      },
      error: (error) => {
        console.error('Error creating new conversation:', error);
      }
    });
  }

  // Add missing methods for template
  startNewConversation() {
    this.newChat();
  }

  getFormattedTime(message: Message): string {
    return this.formatTimestamp(message.timestamp);
  }

  callCrisisLine() {
    window.open('tel:988', '_self');
  }

  openResource(resource: MentalHealthResource) {
    window.open(resource.url, '_blank');
  }

  getResourceTypeColor(type: string): string {
    switch (type) {
      case 'hotline': return '#dc3545';
      case 'therapy': return '#007bff';
      case 'article': return '#28a745';
      case 'exercise': return '#ffc107';
      default: return '#6c757d';
    }
  }

  getResourceTypeIcon(type: string): string {
    switch (type) {
      case 'hotline': return '📞';
      case 'therapy': return '💬';
      case 'article': return '📄';
      case 'exercise': return '🧘';
      default: return '📋';
    }
  }

  onInputChange() {
    this.onMessageInput();
  }

  selectSuggestion(suggestion: string) {
    this.sendQuickSuggestion(suggestion);
  }

  // Add missing trackBy function for performance
  trackByFn(index: number, item: Message): any {
    return item.id || index;
  }

  // Add crisis detection method
  hasCrisisMessages(): boolean {
    return this.lastAnalysis?.crisis_detected || false;
  }

  clearChat() {
    // Clear messages but keep the conversation
    this.messages = [{
      content: "Chat cleared. How can I help you today?",
      sender: 'bot',
      timestamp: new Date().toISOString()
    }];
    this.lastAnalysis = null;
    this.currentMessage = '';
    this.characterCount = 0;
  }

  toggleAIDebug() {
    this.showAIDebug = !this.showAIDebug;
  }

  getSentimentColor(sentiment?: any): string {
    if (!sentiment) return '#6c757d';
    
    const compound = sentiment.compound || 0;
    if (compound > 0.1) return '#28a745'; // Green for positive
    if (compound < -0.1) return '#dc3545'; // Red for negative
    return '#ffc107'; // Yellow for neutral
  }

  getSeverityColor(severity?: string): string {
    switch (severity) {
      case 'high': return '#dc3545';
      case 'medium': return '#ffc107';
      case 'low': return '#28a745';
      default: return '#6c757d';
    }
  }

  formatTimestamp(timestamp?: string): string {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
}