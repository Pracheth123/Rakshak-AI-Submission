import asyncio
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# --- SCENARIO DATA ---
# This simulates the "Cyber Security" scam call flow from your screenshots.
# In the future, this is where you would plug in real AI models.
SCENARIO_TRANSCRIPTS = [
    {
        "speaker": "Abhinav Marte", 
        "text": "Hello, am I speaking with the registered user? This is Abhinav Marte calling from the Cyber Security Division.", 
        "role": "customer"
    },
    {
        "speaker": "You", 
        "text": "Who? I didn't make any request. Which bank is this?", 
        "role": "agent"
    },
    {
        "speaker": "Abhinav Marte", 
        "text": "We have detected unusual activity. I need you to verify your card number immediately to prevent blocking.", 
        "role": "customer"
    },
    {
        "speaker": "System", 
        "text": "CRITICAL ALERT: Sensitive Info Request Detected.", 
        "role": "system"
    },
]

@app.websocket("/listen")
async def websocket_endpoint(websocket: WebSocket):
    print("New Client Requesting Connection...")
    await websocket.accept()
    print("Connection Established.")
    
    try:
        transcript_index = 0
        
        # Keep the connection alive loop
        while True:
            # 1. Receive Audio Stream (Buffer)
            # Your frontend sends audio blobs every 250ms. We must read them to keep the pipe clear.
            # In a real app, you would pass 'data' to a Speech-to-Text model.
            data = await websocket.receive_bytes()
            
            # 2. Simulate Intelligence (Slowly send back transcript lines)
            # We use a random check so it doesn't spam the chat instantly.
            if transcript_index < len(SCENARIO_TRANSCRIPTS) and random.random() < 0.05:
                item = SCENARIO_TRANSCRIPTS[transcript_index]
                
                # Logic to handle System Alerts vs. Chat Messages
                if item["role"] == "system":
                    # Send Transcript Alert
                    await websocket.send_json({
                        "type": "transcript",
                        "speaker": "System",
                        "text": item["text"],
                        "role": "system"
                    })
                    # Send Threat Level Update (Red Alert)
                    await websocket.send_json({
                        "type": "sentiment",
                        "label": "Critical Threat",
                        "score": 95,
                        "color": "bg-red-500"
                    })
                else:
                    # Send Standard Chat Message
                    await websocket.send_json({
                        "type": "transcript",
                        "speaker": item["speaker"],
                        "text": item["text"],
                        "role": item["role"]
                    })
                
                transcript_index += 1
            
            # Brief pause to prevent CPU overload
            await asyncio.sleep(0.01)

    except WebSocketDisconnect:
        print("Client Disconnected")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)