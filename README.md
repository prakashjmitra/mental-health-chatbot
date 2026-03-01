# Mental Health Support Chatbot

A conversational AI application that provides personalized coping strategies, mental health resources, and intelligent dialogue through natural language processing. Built with Django, Angular, and spaCy.

## Overview
<img width="992" height="910" alt="Screenshot 2026-02-28 at 8 40 52 PM" src="https://github.com/user-attachments/assets/51ea0248-f622-4c67-a55f-ec60bea96654" />


This project explores how NLP-driven intent classification can be used to provide accessible, real-time mental health support. The chatbot analyzes user inputs to identify emotional states and conversational intent, then dynamically routes users to appropriate resources and coping strategies.

## Technical Approach

### NLP Pipeline
1. **Preprocessing** — User input is tokenized and normalized using spaCy's language model.
2. **Intent Classification** — A custom intent handler built on spaCy classifies user messages into categories (e.g., anxiety, stress, crisis, general wellness).
3. **Resource Matching** — Based on the classified intent, the system retrieves tailored mental health resources, coping strategies, or escalation prompts from a structured knowledge base.
4. **Crisis Detection** — A separate detection layer flags high-risk language patterns and surfaces emergency contact options when urgent help may be needed.

### Architecture
| Layer | Technology |
|-------|------------|
| Frontend | Angular |
| Backend | Django REST Framework |
| NLP Engine | spaCy + custom intent handler |
| API Design | RESTful with CORS configuration |
| Deployment | Vercel |

## Key Features

- **Intent-Driven Dialogue** — NLP-based classification powers contextual responses rather than simple keyword matching.
- **Crisis Detection** — Identifies urgent language patterns and provides emergency contact options.
- **Daily Check-ins** — Tracks emotional well-being over time to surface trends.
- **Privacy-First Design** — No sign-up required; data handled with user anonymity in mind.

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 16+
- Docker & Docker Compose

### Installation
```bash
git clone https://github.com/yourusername/mental-health-chatbot.git
cd mental-health-chatbot
```


## Future Work

- **LLM Integration** — Explore replacing or augmenting the spaCy intent classifier with a large language model for more nuanced, open-ended dialogue and deeper mental health assessment.
- **Improved Assessment** — Incorporate validated mental health screening instruments (e.g., PHQ-9, GAD-7) to provide more clinically grounded assessments.
- **Longitudinal Analysis** — Leverage daily check-in data to identify emotional trends and provide proactive support.
- **Multimodal Input** — Investigate incorporating voice or physiological signals from wearable sensors to complement text-based interaction.

## Contact

**Prakash Mitra**
B.S. Computer Science, Georgia Institute of Technology (Expected May 2027)
pmitra35@gatech.edu
