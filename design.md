# Rakshak AI - Design Document

## Project Overview

Rakshak AI is a real-time voice scam detection system that analyzes live phone conversations to identify potential fraud attempts. The system uses speech-to-text transcription combined with AI-powered threat analysis to protect users from voice phishing (vishing) attacks.

## System Architecture

### Technology Stack

**Backend:**
- FastAPI (Python web framework)
- WebSocket for real-time bidirectional communication
- Deepgram API (Speech-to-Text transcription)
- Groq LLM (AI threat analysis using Llama 3.1)
- Python-dotenv for configuration management

**Frontend:**
- Single-page HTML application
- TailwindCSS for styling with glassmorphism design
- Vanilla JavaScript for interactivity
- WebSocket client for real-time communication
- MediaRecorder API for audio capture

### Core Components

#### 1. Backend Services

**main.py - WebSocket Server**
- Handles WebSocket connections at `/listen` endpoint
- Manages audio stream from client
- Integrates Deepgram for live transcription
- Coordinates asynchronous AI analysis
- Sends real-time alerts to frontend

**ai_engine.py - Threat Detection Engine**
- ScamProtector class for AI-powered analysis
- Uses Groq's Llama 3.1 model for threat assessment
- Analyzes transcribed text for scam indicators
- Returns structured threat data with confidence scores
- Minimum 5-character threshold for analysis

**config.py - Configuration Management**
- Loads environment variables
- Manages API keys (Deepgram, Groq, AWS)
- Configurable service toggles

#### 2. Frontend Application

**Landing Page**
- Interactive "reveal" effect showing scammer transformation
- Cursor-following spotlight effect
- Animated neural network background
- Call-to-action for system access

**Authentication System**
- Login/Signup forms with tab switching
- Session management via localStorage
- Profile initialization with user initials

**Permissions Screen**
- Privacy policy and consent information
- Microphone access request
- Transparency about AI limitations

**Dashboard**
- Real-time transcript display
- Threat level visualization
- Live audio monitoring indicators
- Safety protocol checklist
- Call timer and session controls

## Data Flow

### 1. Audio Capture & Transcription
```
User Microphone → MediaRecorder → WebSocket Client → 
FastAPI Server → Deepgram API → Transcript
```

### 2. AI Analysis Pipeline
```
Transcript → ScamProtector.analyze() → Groq LLM → 
Threat Assessment → WebSocket Response → Frontend Alert
```

### 3. Real-time Updates
```
Backend sends two message types:
- "transcript": Display conversation text
- "sentiment": Update threat indicators
```

## Key Features

### Real-time Threat Detection
- Continuous audio stream processing
- Instant transcript generation
- Background AI analysis (non-blocking)
- Visual and text-based alerts

### Threat Classification
- **Safe**: Low risk (0-30% score, green indicator)
- **Suspicious**: Medium risk (31-70% score, orange indicator)
- **Critical Threat**: High risk (71-100% score, red indicator)

### User Interface Elements
- Glassmorphism design with backdrop blur
- Dark/light mode toggle
- Animated threat level bar
- Live audio visualization
- Pulsing microphone indicator
- Neural network particle background

### Alert System
- In-chat system alerts with threat details
- Keyword triggers display
- Action buttons (Block Call, Mark Safe)
- Toast notifications for system events

## Security & Privacy

### Data Handling
- Ephemeral audio processing (no recording storage)
- Real-time analysis only
- No PII storage in prototype
- Session-based authentication

### Transparency
- AI decision logging to console
- Confidence scores displayed
- Explicit user consent required
- Clear prototype limitations stated

## AI Analysis Logic

### Prompt Engineering
The system uses structured prompts to analyze conversation snippets:
- Identifies scam indicators
- Extracts trigger keywords from actual text
- Provides confidence scoring
- Returns JSON-formatted threat data

### Response Format
```json
{
  "is_threat": boolean,
  "label": "Safe|Suspicious|CRITICAL THREAT",
  "score": 0-100,
  "confidence": 0-100,
  "color": "bg-emerald-500|bg-orange-500|bg-red-500",
  "reason": "Explanation",
  "triggers": ["keyword1", "keyword2"]
}
```

## Performance Optimizations

### Asynchronous Processing
- Non-blocking AI analysis using `asyncio.create_task()`
- Prevents WebSocket timeout during LLM processing
- Instant transcript delivery to frontend

### Efficient Communication
- 250ms audio chunks for optimal latency
- Minimal JSON payloads
- WebSocket connection reuse

## User Experience Flow

1. **Landing** → Interactive reveal effect introduces concept
2. **Authentication** → Quick login/signup
3. **Permissions** → Consent and microphone access
4. **Dashboard** → Live monitoring interface
5. **Analysis** → Real-time threat detection during call
6. **Alerts** → Immediate warnings with actionable options

## Design Patterns

### Frontend Architecture
- View-based navigation system
- State management via DOM manipulation
- Event-driven WebSocket communication
- Modular JavaScript functions

### Backend Architecture
- Async/await pattern throughout
- Event-driven WebSocket handlers
- Separation of concerns (transcription vs analysis)
- Error handling with graceful degradation

## Styling & Aesthetics

### Visual Theme
- Modern glassmorphism with backdrop blur
- Gradient accents (indigo to purple)
- Smooth transitions and animations
- Responsive layout with Tailwind utilities

### Interactive Elements
- Animated orbs in background
- Particle network connections
- Pulsing indicators for active states
- Smooth fade transitions between views

## Future Enhancements

### Planned Features
- AWS integration for scalable deployment
- Multi-language support
- Historical call analysis
- Advanced reporting dashboard
- Machine learning model fine-tuning
- Call recording (with explicit consent)

### Scalability Considerations
- AWS infrastructure ready (config placeholders)
- Modular service architecture
- API key rotation support
- Load balancing preparation

## Development Setup

### Requirements
```
fastapi==0.128.3
deepgram-sdk==3.11.0
groq (via dependencies)
python-dotenv==1.2.1
uvicorn==0.40.0
websockets==16.0
```

### Environment Variables
- `DEEPGRAM_API_KEY`: Speech-to-text service
- `GROQ_API_KEY`: LLM analysis service
- `AWS_*`: Future cloud deployment (optional)

### Running the Application
```bash
# Backend
python main.py  # Starts on localhost:8000

# Frontend
# Open Rakshak.html in browser
# Ensure WebSocket connects to ws://localhost:8000/listen
```

## Technical Challenges Solved

1. **WebSocket Timeout Prevention**: Moved AI analysis to background tasks
2. **Real-time Synchronization**: Instant transcript + delayed analysis
3. **Theme Consistency**: Persistent dark/light mode across sessions
4. **Audio Streaming**: Efficient chunking with MediaRecorder
5. **Responsive Alerts**: Non-blocking UI updates during analysis

## Prototype Limitations

- Free-tier API usage (rate limits apply)
- No persistent database
- Single-user sessions only
- English language only
- Requires modern browser with WebSocket support
- No mobile optimization

## Conclusion

Rakshak AI demonstrates a functional prototype for real-time voice scam detection using modern web technologies and AI. The system successfully combines speech recognition, natural language processing, and an intuitive user interface to provide immediate threat awareness during phone conversations.
