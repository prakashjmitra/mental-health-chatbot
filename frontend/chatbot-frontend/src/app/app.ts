import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatComponent } from './components/chat/chat';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ChatComponent],  // Removed HttpClientModule
  template: `<app-chat></app-chat>`,
  styleUrls: ['./app.css']
})
export class AppComponent {
  title = 'mental-health-chatbot';
}