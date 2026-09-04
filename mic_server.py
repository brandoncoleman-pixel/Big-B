import asyncio
import struct
import websockets

PCM_FILE = "/tmp/vnc-microphone.pcm"

async def handle(websocket):
    print("Microphone connected")

    with open(PCM_FILE, "wb", buffering=0) as pcm:
        async for message in websocket:
            if isinstance(message, bytes):
                # Browser sends Float32 mono samples.
                count = len(message) // 4
                samples = struct.unpack("<" + "f" * count, message)

                # Convert Float32 (-1.0..1.0) to signed 16-bit PCM.
                output = bytearray()
                for sample in samples:
                    sample = max(-1.0, min(1.0, sample))
                    value = int(sample * 32767)
                    output += struct.pack("<h", value)

                pcm.write(output)

    print("Microphone disconnected")

async def main():
    print("Microphone server listening on port 6081")
    async with websockets.serve(handle, "0.0.0.0", 6081):
        await asyncio.Future()

asyncio.run(main())
