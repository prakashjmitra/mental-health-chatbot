import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Message } from '../../services/api.service';

@Component({
  selector: 'app-message',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './message.html',
  styleUrls: ['./message.css']
})
export class MessageComponent {
  @Input() message!: Message;

  get isUser(): boolean {
    return this.message.sender === 'user';
  }

  get isBot(): boolean {
    return this.message.sender === 'bot';
  }

  get formattedTime(): string {
    if (this.message.timestamp) {
      return new Date(this.message.timestamp).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      });
    }
    return '';
  }
}