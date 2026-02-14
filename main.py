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
        # Connect to Deepgram
        deepgram = DeepgramClient(settings.DEEPGRAM_API_KEY)
        dg_connection = deepgram.listen.asyncwebsocket.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if not sentence: return
            
            print(f"🗣️  Heard: {sentence}")

            # Send Transcript
            await websocket.send_json({
                "type": "transcript", 
                "speaker": "Caller", 
                "text": sentence, 
                "role": "customer"
            })

            # Analyze
            # Analyze
            # 2. Analyze using Modular Engine
            threat = await detector.analyze(sentence)
            if threat:
                # Send Visual Alert (Now includes confidence)
                await websocket.send_json({
                    "type": "sentiment",
                    "label": threat["label"],
                    "score": threat["score"],
                    "confidence": threat.get("confidence", 85),
                    "color": threat["color"]
                })
                
                # Send System Chat Alert (Now includes transparent reasoning)
                triggers_str = ", ".join(threat.get("triggers", []))
                await websocket.send_json({
                    "type": "transcript",
                    "speaker": "Rakshak AI",
                    "text": f"🛡️ ALERT: {threat['reason']}. <br><span class='text-xs opacity-75'>Triggered by keywords: [ {triggers_str} ]</span>",
                    "role": "system"
                })

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        options = LiveOptions(model="nova-2", language="en-US", smart_format=True)
        await dg_connection.start(options)
        print("🟢 Service Ready")

        while True:
            data = await websocket.receive_bytes()
            await dg_connection.send(data)

    except WebSocketDisconnect:
        print("🔴 Client Disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'dg_connection' in locals():
            await dg_connection.finish()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)