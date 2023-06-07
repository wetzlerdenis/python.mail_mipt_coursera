# week6
# Task 1 Server for receiving metrics

"""
Необходимо реализовать серверную часть.
Требоания 
1) По запросу put требуется сохранять метрики в структурах данных в памяти процесса. 
2) По запросу get сервер обязан отдавать данные в правильной последовательности. 
3) При работе с клиентом сервер должен поддерживать сессии, соединение с 
клиентом между запросами не должно "разрываться".
4) На верхнем уровне модуля должна быть объявлена функция run_server(host, port) 
5) Все запросы будут выполняться с таймаутом
6) должен уметь обрабатывать запросы от нескольких клиентов одновременно.
7) должен отдавать клиенту ошибку в формате, оговоренном в протоколе. 
В этих случаях работа сервера не должна завершаться аварийно.

Пример tcp-сервера на asyncio:
1) Данный код создает tcp-соединение для адреса 127.0.0.1:8181 
2) слушает все входящие запросы
3) При подключении клиента будет создан новый экземпляр класса ClientServerProtocol, 
4) при поступлении новых данных вызовется метод объекта - data_received

Внутри asyncio.Protocol спрятана вся магия обработки запросов через корутины, 
остается реализовать протокол взаимодействия между клиентом и сервером.
"""

import asyncio

err_response = 'error\nwrong command\n\n'
ok_response = 'ok\n\n'
stor = ''

def better_process_data(data):
    try:
        #processing empty request like '\n'
        request, payload = data.split(' ',1)
    except ValueError:
        request = payload = data.split()
    
    if request == 'get' and len(data.split()) == 2:
        return process_get(payload)
    elif request == 'put' and len(data.split()) == 4:
        return process_put(payload)
    else: 
        return err_response


def process_get(payload):
    payload = payload.strip()

    if not payload:
        pass
    elif payload == '*':
        return 'ok\n' + stor + '\n'
    else:
        return 'ok\n' + find_all_records(payload) + '\n'


def find_all_records(key):
    extract = ''
    for record in stor.splitlines():
        print('record: ',record)
        if key == record.split()[0]:
            extract += record + '\n'
    return extract 


def process_put(payload):

    new_value = payload.split()[1]
    new_timestamp = payload.split()[2]

    try:
        value = float(new_value)
        timestamp = int(new_timestamp)
    except ValueError:
        return err_response
    else:
        payload = payload.replace(new_value, str(float(new_value)))
        return update_storage(payload)


def update_storage(payload):
    key = payload.split()[0]
    new_t = payload.split()[2]
    global stor

    if stor.find(key) == -1:
        stor += payload
    else:
        b = 0
        while stor.find(key, b) != -1:

            a = stor.find(key, b)
            b = stor.find('\n', a)
            t = stor[a:b + 1].split()[2]

            if t == new_t:
                stor = stor.replace(stor[a:b], payload.strip())
                break
        
        if t != new_t:
            stor += payload

    return ok_response


class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
            
    def data_received(self, data):
        message = data.decode()
        print('Received: ',message)

        resp = better_process_data(message)

        print('Send: ', resp)
        self.transport.write(resp.encode())

    def connection_lost(self, exc):
        return super().connection_lost(exc)

def run_server(host,port):
    loop = asyncio.get_event_loop()

    coro = loop.create_server(
        ClientServerProtocol,
        host,
        port
        )
    
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
        print('running forever')
    except KeyboardInterrupt:
        print('closing everything:\n')
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == "__main__":
    run_server("127.0.0.1", 10001)