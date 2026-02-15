# 🛡️ Rakshak AI

**Unmask the Hidden Danger in Every Call.**

Rakshak AI is an active-defense cybersecurity prototype designed to detect and unmask voice phishing (vishing) and social engineering attacks in real-time.

Unlike traditional security measures that rely on blocking known spam numbers, scammers today constantly spoof caller IDs. Rakshak AI acts as an invisible shield during a live call, analyzing the _context_ and _intent_ of the conversation to warn users before they compromise their financial or personal security.

## ✨ Key Features

- **Real-Time Active Defense:** Captures live phone audio via WebSockets and transcribes it in 250ms chunks.
- **Contextual AI Brain:** Uses an LLM to understand the psychological manipulation tactics (e.g., urgency, threats, sensitive info requests) rather than just simple keyword matching.
- **Explainable Alerts:** Does not operate as a "black box." When a threat is detected, the UI explains _why_ the alert was triggered and lists the exact keywords.
- **Human-in-the-Loop (HITL):** Empowers the user with an interactive Command Center dashboard, allowing them to instantly "Block & Disconnect" or "Mark as Safe" to log system feedback.
- **Privacy-First Design:** Audio is processed ephemerally in memory. No recordings or personally identifiable information (PII) are stored.

## 🛠️ Technical Architecture

- **Frontend UI:** HTML5, Vanilla JavaScript, Tailwind CSS, Lucide Icons. Features an immersive Glassmorphism design and an interactive HTML5 Neural Network canvas.
- **Backend Server:** FastAPI (Python) asynchronous server handling bi-directional WebSocket streams to prevent API blocking.
- **Speech-to-Text (ASR):** Deepgram Nova-2 for ultra-low latency live transcription.
- **AI/LLM Engine:** Groq API running `llama-3.1-8b-instant` for high-speed intent evaluation.

## 📂 Repository Contents

- `design.md`: Detailed system architecture, data flow, and UI/UX design choices.
- `requirements.md`: Comprehensive list of functional/non-functional requirements and technical dependencies.

---
