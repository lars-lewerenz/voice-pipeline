import asyncio
import queue
import sys
from typing import Any, Optional

import sounddevice as sd
from websockets.asyncio.client import ClientConnection, connect

from voice_pipeline.config import settings

tx_queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=settings.tx_queue_maxsize) # Micr
rx_queue: queue.Queue[bytes] = queue.Queue()  # Network -> Speaker

loop: Optional[asyncio.AbstractEventLoop] = None


def _enqueue_tx_frame(data: bytes) -> None:
    if tx_queue.full():
        try:
            tx_queue.get_nowait()
        except asyncio.QueueEmpty:
            pass
    try:
        tx_queue.put_nowait(data)
    except asyncio.QueueFull:
        pass


def audio_callback(
    indata: memoryview,
    outdata: memoryview,
    frames: int,
    time: Any,
    status: sd.CallbackFlags,
):
    if status:
        print(f"Audio Warning: {status}", file=sys.stderr)

    if loop is not None:
        loop.call_soon_threadsafe(_enqueue_tx_frame, bytes(indata))

    try:
        data: bytes = rx_queue.get_nowait()
        outdata[:] = data
    except queue.Empty:
        outdata[:] = b"\x00" * len(outdata)


async def send_audio(ws: ClientConnection) -> None:
    while True:
        data: bytes = await tx_queue.get()
        await ws.send(data)


async def receive_audio(ws):
    async for message in ws:
        if isinstance(message, bytes):
            rx_queue.put_nowait(message)


async def _run() -> None:
    global loop
    loop = asyncio.get_running_loop()

    stream = sd.RawStream(
        samplerate=settings.sample_rate,
        blocksize=settings.blocksize,
        channels=settings.channels,
        dtype=settings.dtype,
        latency=settings.portaudio_latency,
        callback=audio_callback,
    )

    with stream:
        async with connect(
            settings.ws_url,
            compression="deflate" if settings.ws_compression else None,
            max_queue=settings.ws_max_queue,
        ) as ws:
            print("Connected. Speak into the microphone...")

            async with asyncio.TaskGroup() as tg:
                tg.create_task(send_audio(ws))
                tg.create_task(receive_audio(ws))


def main() -> None:
    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        print("\nClient terminated.")


if __name__ == "__main__":
    main()
