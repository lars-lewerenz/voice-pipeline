# voice-pipeline

Small WebSocket echo path: microphone from the client is sent to the server and played back on the client (for trying latency and audio setup).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) and Python 3.12+
- A working mic and speakers (the client uses [sounddevice](https://python-sounddevice.readthedocs.io/), which needs [PortAudio](https://www.portaudio.com/) on your system)

## Setup

From the repository root:

```bash
uv sync
```

Optional: copy `.env.example` to `.env` and adjust `VOICE_*` variables (host, port, audio block size, etc.).

## Run with uv

Use two terminals, both in the project root. Start the server first, then the client.

**Server**

```bash
uv run server
```

**Client**

```bash
uv run client
```

You should hear your microphone input echoed back after network round-trip latency.
