from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

from voice_pipeline.config import settings

app = FastAPI()


@app.websocket(settings.ws_path)
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


def main() -> None:
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
