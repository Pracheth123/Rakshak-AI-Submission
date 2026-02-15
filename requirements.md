# Rakshak AI - Requirements Document

## 1. Project Vision

### 1.1 Purpose
Rakshak AI aims to protect individuals from voice phishing (vishing) scams by providing real-time AI-powered threat detection during phone conversations.

### 1.2 Target Users
- Elderly individuals vulnerable to phone scams
- Financial institution customers
- General public receiving suspicious calls
- Law enforcement and fraud prevention teams

### 1.3 Success Criteria
- Detect scam indicators within 5 seconds of suspicious language
- Achieve 85%+ accuracy in threat classification
- Maintain <500ms latency for transcript display
- Provide actionable alerts with clear explanations

## 2. Functional Requirements

### 2.1 User Authentication

#### FR-1.1: User Login
- Users must be able to log in with email and password
- System shall validate credentials before granting access
- Session shall persist across page refreshes
- Invalid credentials shall display error message

#### FR-1.2: User Registration
- Users must be able to create new accounts
- System shall store user information locally
- Email format validation required
- Password minimum length: 4 characters

#### FR-1.3: Session Management
- System shall maintain active sessions using localStorage
- Users shall be able to log out manually
- Profile initials shall display in dashboard header
- Automatic redirect to dashboard if session exists

### 2.2 Permissions & Consent

#### FR-2.1: Microphone Access
- System must request microphone permission before analysis
- Users must explicitly grant consent
- Permission status shall be stored locally
- Denial shall prevent access to dashboard

#### FR-2.2: Privacy Disclosure
- System shall display privacy policy before access
- Users must acknowledge data handling practices
- Clear statement about ephemeral processing
- Transparency about AI limitations and false positives

### 2.3 Audio Processing

#### FR-3.1: Live Audio Capture
- System shall capture audio from user's microphone
- Audio shall be streamed in 250ms chunks
- MediaRecorder API shall be used for capture
- Audio stream shall stop when call ends

#### FR-3.2: Speech-to-Text Transcription
- System shall transcribe audio in real-time using Deepgram
- Transcription shall use Nova-2 model
- Language: English (US)
- Smart formatting shall be enabled

#### FR-3.3: Transcript Display
- Transcripts shall appear instantly in chat interface
- Speaker labels shall distinguish caller vs system
- Messages shall auto-scroll to latest
- Transcript history shall persist during session

### 2.4 AI Threat Analysis

#### FR-4.1: Real-time Analysis
- System shall analyze each transcript segment
- Minimum text length: 5 characters
- Analysis shall run asynchronously (non-blocking)
- Results shall be processed within 3 seconds

#### FR-4.2: Threat Classification
- System shall classify threats into three levels:
  - **Safe**: 0-30% threat score (green)
  - **Suspicious**: 31-70% threat score (orange)
  - **Critical Threat**: 71-100% threat score (red)

#### FR-4.3: Threat Detection Criteria
System shall detect the following scam indicators:
- Urgency tactics ("act now", "limited time")
- Requests for sensitive information (SSN, passwords, banking)
- Impersonation of authorities (IRS, police, tech support)
- Payment demands (gift cards, wire transfers, cryptocurrency)
- Threats or intimidation language
- Too-good-to-be-true offers
- Verification code requests

#### FR-4.4: Analysis Output
- System shall provide threat label
- System shall calculate confidence score (0-100%)
- System shall extract trigger keywords from actual text
- System shall provide human-readable explanation

### 2.5 Alert System

#### FR-5.1: Visual Alerts
- Threat level bar shall update in real-time
- Color coding shall match threat severity
- Confidence percentage shall display
- Smooth animations for state transitions

#### FR-5.2: In-Chat Alerts
- System alerts shall appear in transcript feed
- Alerts shall include threat explanation
- Trigger keywords shall be displayed
- Alerts shall be visually distinct from regular messages

#### FR-5.3: Action Buttons
- "Block Call" button shall end session immediately
- "Mark Safe" button shall dismiss alert
- Actions shall provide user feedback via toast notifications
- Dismissed alerts shall reduce opacity

### 2.6 Dashboard Features

#### FR-6.1: Call Controls
- "Start Live Analysis" button to begin monitoring
- "End Session" button to stop analysis
- Call timer displaying MM:SS format
- Live audio visualization during active calls

#### FR-6.2: Status Indicators
- System online/offline status
- Microphone active indicator with pulse animation
- Connection status to backend
- Real-time audio level bars

#### FR-6.3: Safety Protocols Panel
- Display of active monitoring features:
  - Caller verification status
  - Sensitive information detection
  - Urgency tactics monitoring

### 2.7 User Interface

#### FR-7.1: Landing Page
- Interactive reveal effect showing scam concept
- Cursor-following spotlight effect
- Animated background with neural network particles
- Clear call-to-action buttons

#### FR-7.2: Theme Support
- Light and dark mode toggle
- Theme preference persistence
- System theme detection on first load
- Smooth transitions between themes

#### FR-7.3: Responsive Design
- Support for desktop browsers (1280px+)
- Glassmorphism design with backdrop blur
- Accessible color contrast ratios
- Smooth animations and transitions

#### FR-7.4: Navigation
- View-based navigation system
- Back button on authentication page
- Logout functionality from dashboard
- Automatic view switching based on state

## 3. Non-Functional Requirements

### 3.1 Performance

#### NFR-1.1: Latency
- Transcript display: <500ms from speech
- AI analysis completion: <3 seconds
- WebSocket message delivery: <100ms
- Page load time: <2 seconds

#### NFR-1.2: Throughput
- Support continuous audio streaming
- Handle 4 audio chunks per second
- Process multiple transcript segments concurrently

### 3.2 Reliability

#### NFR-2.1: Availability
- Backend uptime: 99% during demo period
- Graceful degradation on API failures
- Error messages for connection issues
- Automatic reconnection attempts

#### NFR-2.2: Error Handling
- WebSocket disconnection handling
- Microphone access denial handling
- API timeout handling
- Invalid response format handling

### 3.3 Security

#### NFR-3.1: Data Privacy
- No audio recording storage
- Ephemeral processing only
- No transmission of PII to third parties
- Secure WebSocket connections (WSS in production)

#### NFR-3.2: API Security
- API keys stored in environment variables
- No hardcoded credentials in code
- Rate limiting awareness
- Secure key rotation support

### 3.4 Usability

#### NFR-4.1: Accessibility
- Clear visual hierarchy
- High contrast text
- Icon labels for clarity
- Keyboard navigation support

#### NFR-4.2: User Experience
- Intuitive interface requiring no training
- Clear feedback for all actions
- Consistent design language
- Helpful error messages

### 3.5 Maintainability

#### NFR-5.1: Code Quality
- Modular architecture
- Clear separation of concerns
- Comprehensive inline comments
- Consistent naming conventions

#### NFR-5.2: Extensibility
- Pluggable AI model support
- Configurable threat thresholds
- Multi-language support preparation
- AWS integration readiness

### 3.6 Compatibility

#### NFR-6.1: Browser Support
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

#### NFR-6.2: Technology Requirements
- WebSocket support required
- MediaRecorder API support required
- ES6+ JavaScript support required
- CSS Grid and Flexbox support required

## 4. System Requirements

### 4.1 Backend Environment

#### Hardware
- Minimum 2GB RAM
- 1 CPU core
- 10GB storage
- Stable internet connection

#### Software
- Python 3.8+
- pip package manager
- Virtual environment support

### 4.2 Frontend Environment

#### Client Requirements
- Modern web browser (see NFR-6.1)
- Microphone hardware
- Stable internet connection (1 Mbps+)
- JavaScript enabled

### 4.3 External Services

#### Required APIs
- Deepgram API (Speech-to-Text)
  - Free tier: 45,000 minutes/year
  - Nova-2 model access
  
- Groq API (LLM Analysis)
  - Free tier: Rate limited
  - Llama 3.1-8B model access

#### Optional Services
- AWS (Future deployment)
  - EC2 for hosting
  - S3 for storage
  - CloudWatch for monitoring

## 5. Data Requirements

### 5.1 Data Models

#### User Session
```javascript
{
  email: string,
  name: string,
  timestamp: datetime
}
```

#### Transcript Message
```javascript
{
  type: "transcript",
  speaker: string,
  text: string,
  role: "customer" | "system"
}
```

#### Threat Assessment
```javascript
{
  type: "sentiment",
  is_threat: boolean,
  label: string,
  score: number (0-100),
  confidence: number (0-100),
  color: string,
  reason: string,
  triggers: string[]
}
```

### 5.2 Data Storage

#### Local Storage
- User session data
- Theme preference
- Microphone permission status
- User account information (prototype only)

#### No Persistent Storage
- Audio streams (ephemeral)
- Transcripts (session only)
- Threat analysis results (session only)

## 6. Integration Requirements

### 6.1 Deepgram Integration
- WebSocket connection to Deepgram API
- Live transcription events handling
- Audio format: Raw PCM or WebM
- Automatic reconnection on failure

### 6.2 Groq Integration
- Async HTTP requests to Groq API
- JSON response format enforcement
- Temperature: 0.1 (deterministic)
- Model: llama-3.1-8b-instant

### 6.3 WebSocket Communication
- Bidirectional real-time messaging
- JSON message format
- Connection lifecycle management
- Heartbeat/keepalive (if needed)

## 7. Constraints & Limitations

### 7.1 Technical Constraints
- Single-user sessions only
- No call recording capability
- English language only
- Desktop browser focus (no mobile optimization)

### 7.2 API Limitations
- Deepgram free tier rate limits
- Groq API rate limits
- No offline functionality
- Requires active internet connection

### 7.3 Prototype Limitations
- No production database
- No user authentication backend
- No call history storage
- No multi-language support
- No WCAG compliance validation

## 8. Future Requirements

### 8.1 Phase 2 Features
- Multi-language support (Spanish, Hindi, Mandarin)
- Mobile application (iOS/Android)
- Call recording with consent
- Historical analysis dashboard
- User feedback mechanism
- Admin panel for monitoring

### 8.2 Phase 3 Features
- Machine learning model fine-tuning
- Custom threat pattern training
- Integration with phone systems
- API for third-party integration
- Advanced reporting and analytics
- Team collaboration features

### 8.3 Enterprise Features
- Multi-tenant architecture
- Role-based access control
- Compliance reporting (GDPR, CCPA)
- SLA guarantees
- Dedicated support
- Custom deployment options

## 9. Testing Requirements

### 9.1 Functional Testing
- User authentication flows
- Microphone permission handling
- Audio capture and streaming
- Transcript accuracy
- Threat detection accuracy
- Alert triggering
- UI state transitions

### 9.2 Performance Testing
- Latency measurements
- Concurrent user handling
- Memory leak detection
- WebSocket stability
- API response times

### 9.3 Security Testing
- API key exposure checks
- XSS vulnerability testing
- Data transmission security
- Session management security

### 9.4 Usability Testing
- User flow completion rates
- Error recovery testing
- Accessibility compliance
- Cross-browser compatibility

## 10. Documentation Requirements

### 10.1 User Documentation
- Quick start guide
- Feature overview
- Privacy policy
- FAQ section
- Troubleshooting guide

### 10.2 Technical Documentation
- API documentation
- Architecture diagrams
- Deployment guide
- Configuration reference
- Development setup guide

### 10.3 Compliance Documentation
- Data handling procedures
- Privacy impact assessment
- Security audit reports
- Terms of service
- Consent forms

## 11. Success Metrics

### 11.1 Performance Metrics
- Average threat detection time: <3s
- Transcript accuracy: >90%
- System uptime: >99%
- False positive rate: <15%

### 11.2 User Metrics
- User satisfaction score: >4/5
- Feature adoption rate: >70%
- Session completion rate: >85%
- Error rate: <5%

### 11.3 Business Metrics
- Scams prevented (user reported)
- User retention rate
- API cost per session
- System scalability capacity

## 12. Acceptance Criteria

### 12.1 Minimum Viable Product (MVP)
- ✅ User can log in and access dashboard
- ✅ System captures and transcribes audio in real-time
- ✅ AI analyzes transcripts and detects threats
- ✅ Alerts display with explanations and trigger words
- ✅ Users can start/stop monitoring sessions
- ✅ Theme toggle works correctly
- ✅ System handles errors gracefully

### 12.2 Demo Readiness
- ✅ Landing page with interactive reveal effect
- ✅ Smooth navigation between all views
- ✅ Real-time threat visualization
- ✅ Professional UI with animations
- ✅ Clear privacy disclosures
- ✅ Functional call controls
- ✅ Toast notifications for feedback

### 12.3 Production Readiness (Future)
- ⏳ Scalable cloud deployment
- ⏳ Database integration
- ⏳ User authentication backend
- ⏳ Comprehensive logging
- ⏳ Monitoring and alerting
- ⏳ Load balancing
- ⏳ Backup and recovery procedures
