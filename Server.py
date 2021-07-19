import asyncio
import wave


framerate = 48000

BUFFER = {}


async def save(data, addr):
    wf = wave.open(f'{addr}.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))


HOST, PORT = 'localhost', 9999


class Protocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_running_loop()

    def connection_made(self, transport):
        self.transport = transport

    async def respond(self, data, addr):
        if data == b'Accept':
            print('OK')
            BUFFER.update({addr: []})
        elif data == b'Close':

            self.loop.create_task(save(BUFFER.pop(addr), addr))

        else:
            BUFFER.get(addr).append(data)

    def datagram_received(self, data, addr):

        self.loop.create_task(self.respond(data, addr))


async def main():
    print("Starting UDP server")

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: Protocol(),
        local_addr=('127.0.0.1', 9999))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


asyncio.run(main())
