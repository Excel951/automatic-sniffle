import asyncio
import serial_asyncio

class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can configure serial parameters here
        self.transport.write(b'Hello, world!\n')  # Send some data

    def data_received(self, data):
        print('data received', repr(data))
        self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()

async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await serial_asyncio.create_serial_connection(
        loop, Output, 'COM20', baudrate=9600)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
