from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws")
async def echo_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # yield control back to the event loop while waiting for incoming network packets
            data = await websocket.receive_bytes()

            # immediate echo return of the raw bytes
            await websocket.send_bytes(data)
    except WebSocketDisconnect:
        print("Client disconnected.")
