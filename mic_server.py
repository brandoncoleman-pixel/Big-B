import asyncio
import websockets

PCM_FILE = "/tmp/vnc-microphone.pcm"

async def handle(websocket):
    print("Microphone connected", flush=True)

    with open(PCM_FILE, "wb", buffering=0) as pcm:
        async for message in websocket:
            if isinstance(message, bytes):
                # Browser sends signed 16-bit PCM, mono, 16 kHz.
                pcm.write(message)

    print("Microphone disconnected", flush=True)

async def main():
    print("Microphone server listening on port 6081", flush=True)

    async with websockets.serve(
        handle,
        "0.0.0.0",
        6081,
        max_size=None
    ):
        await asyncio.Future()

asyncio.run(main())
