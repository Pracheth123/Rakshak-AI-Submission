import asyncio
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from ai_engine import ScamProtector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

app = FastAPI()
detector = ScamProtector()

# =========================================================
# SERVE THE FRONTEND UI (For AWS / Cloud Deployment)
# =========================================================
@app.get("/")
async def serve_frontend():
    return FileResponse("Rakshak.html")

# =========================================================
# WEBSOCKET AUDIO STREAMING & AI ANALYSIS
# =========================================================
@app.websocket("/listen")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔵 Frontend Client Connected")

    if not DEEPGRAM_API_KEY:
        print("❌ ERROR: DEEPGRAM_API_KEY is missing from .env")
        return

    try:
        # Initialize Deepgram
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        dg_connection = deepgram.listen.asyncwebsocket.v("1")

        # Define what happens when Deepgram hears speech
        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            
            # Only process final, complete sentences
            if len(sentence) > 0 and result.is_final:
                print(f"🗣️ Deepgram Heard: {sentence}")
                
                # Send text to frontend UI
                await websocket.send_json({
                    "type": "transcript", 
                    "speaker": "Caller", 
                    "text": sentence, 
                    "role": "customer"
                })
                
                # Analyze with AWS Bedrock in the background
                asyncio.create_task(analyze_and_send(sentence, websocket))

        # Helper function to handle AWS Bedrock analysis
        async def analyze_and_send(text, ws):
            threat = await detector.analyze(text)
            if threat:
                # 1. Update Threat Meter
                await ws.send_json({
                    "type": "sentiment",
                    "label": threat.get("label", "Suspicious"),
                    "score": threat.get("score", 50),
                    "confidence": threat.get("confidence", 85),
                    "color": threat.get("color", "bg-orange-500")
                })
                
                # =========================================================
                # BULLETPROOF FAILSAFE FOR SILENT GUARDIAN
                # =========================================================
                action = str(threat.get("action", "")).lower()
                label = str(threat.get("label", "")).upper()
                score = int(threat.get("score", 0))
                
                # If the AI says it's critical OR the score is 90+, FORCE the lockdown
                if action == "silent_guardian" or "CRITICAL" in label or score >= 90:
                    print("🚨 CRITICAL THREAT DETECTED: Forcing Silent Guardian Protocol!")
                    await ws.send_json({
                        "type": "protocol_silent_guardian",
                        "reason": threat.get("reason", "Digital Arrest / Extreme Coercion Detected")
                    })
                else:
                    triggers_str = ", ".join(threat.get("triggers", []))
                    reason = threat.get("reason", "Suspicious activity detected.")
                    await ws.send_json({
                        "type": "transcript",
                        "speaker": "Rakshak AI",
                        "text": f"🛡️ ALERT: {reason} <br><span class='text-xs opacity-75'>Triggers: [ {triggers_str} ]</span>",
                        "role": "system"
                    })

        # Attach the message handler
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        # Configure Deepgram for Hinglish Code-Switching
        options = LiveOptions(
            model="nova-2",
            language="hi",          
            smart_format=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )

        # Start the Deepgram connection
        await dg_connection.start(options)
        print("🟢 Deepgram STT Engine Active")

        # Route audio from Browser -> Python -> Deepgram
        while True:
            data = await websocket.receive_bytes()
            await dg_connection.send(data)
            
    except WebSocketDisconnect:
        print("🔴 Frontend Client Disconnected")
    except Exception as e:
        print(f"❌ WebSocket Error: {e}")
    finally:
        if 'dg_connection' in locals():
            await dg_connection.finish()

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 is crucial so it can be accessed from the public internet!
    uvicorn.run(app, host="0.0.0.0", port=8000)