# asyncio, tcp сервер

import asyncio
async def handle_echo(reader, writer):
    
    data = await reader.read(1024)
    message = data.decode()
    
    addr = writer.get_extra_info("peername")
    print("received %r from %r" % (message, addr))
    
    response = 'ok\n\n'
    
    print(f"Send: {response!r}")
    writer.write(response.encode())
    await writer.drain()

    
loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, "127.0.0.1", 10001,
                            loop=loop)
server = loop.run_until_complete(coro)
print('running until complete')

#будем обрабатывать все входящие соединения, 
# и после того, как мы заакцептили соединение, 
# для каждого соединения будет создана отдельная 
# корутина, и в этой корутине будет выполнена функция

try:
    loop.run_forever()
    print('running forever')
except KeyboardInterrupt:
    print('closing everything:\n')
    server.close()
    print('server closed\n')
    loop.run_until_complete(server.wait_closed())
    loop.close()
    print('closing loop')