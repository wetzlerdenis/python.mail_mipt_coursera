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

class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.storage = ''

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def _save_data(self, metric):
        self.storage += metric
        print('storage increased ',self.storage)

    def _extract_metric(self, payload_key):
        payload_key = payload_key.strip()
        extract = ''

        if not payload_key:
            pass
        elif payload_key == '*':
            extract = self.storage
        else:
            for line in self.storage.splitlines()[:-1]:
                key = line.split()[0]

                if key == payload_key:
                    extract += line
        return extract
            
    def data_received(self, data):
        message = data.decode()
        print('Received: ',message)

        resp = self.process_data(message)

        print('Send: ', resp)
        self.transport.write(resp.encode())

    def connection_lost(self, exc):
        return super().connection_lost(exc)

    def process_data(self, data):

        response = 'error\nwrong command\n\n'

        request, payload = data.split(' ',1)

        if request == 'get' and len(payload.split()) == 1:

            response = 'ok\n' + \
                self._extract_metric(payload_key=payload) + '\n'

        elif request == 'put':
            metric, value, timestamp = payload.split()

            try:
                value = float(value)
                timestamp = int(timestamp)
                response = 'ok\n\n'
                self._save_data(payload)
            except Exception as err:
                print('cannot transform values')

        return response


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

run_server('127.0.0.1', 10001)
