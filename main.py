import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from config import settings
from ai_engine import ScamProtector

app = FastAPI()
detector = ScamProtector()

@app.websocket("/listen")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔵 Client Connected")

    try:
        # --- AUDIO SERVICE ---
        # Current: Deepgram (Easiest for WebSockets)
        # Future Upgrade: Swap with 'Amazon Transcribe Streaming' here
        deepgram = DeepgramClient(settings.DEEPGRAM_API_KEY)
        dg_connection = deepgram.listen.asyncwebsocket.v("1")

        # 1. Handle Incoming Transcripts
        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if not sentence: return
            
            print(f"🗣️  Heard: {sentence}")

            # Send Transcript to UI
            await websocket.send_json({
                "type": "transcript", 
                "speaker": "Caller", 
                "text": sentence, 
                "role": "customer"
            })

            # 2. Analyze using Modular Engine
            threat = detector.analyze(sentence)
            
            if threat:
                # Send Visual Alert
                await websocket.send_json({
                    "type": "sentiment",
                    "label": threat["label"],
                    "score": threat["score"],
                    "color": threat["color"]
                })
                # Send System Chat Alert
                await websocket.send_json({
                    "type": "transcript",
                    "speaker": "Rakshak AI",
                    "text": f"🛡️ ALERT: {threat['reason']}",
                    "role": "system"
                })

        # Register Event
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        # Start Deepgram
        options = LiveOptions(model="nova-2", language="en-US", smart_format=True)
        await dg_connection.start(options)
        print("🟢 Deepgram Live Service Ready")

        # 3. Main Audio Loop (Browser -> Python -> Deepgram)
        while True:
            data = await websocket.receive_bytes()
            await dg_connection.send(data)

    except WebSocketDisconnect:
        print("🔴 Client Disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        if 'dg_connection' in locals():
            await dg_connection.finish()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)