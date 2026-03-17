from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws")
async def echo_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            # yield control back to the event loop while waiting for incoming network packets
            # then: directly echo the data
            async for data in websocket.iter_bytes():
                await websocket.send_bytes(data)
    except WebSocketDisconnect:
        print("Client disconnected.")
