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

class Storage:
    def __init__(self):
        self.data = ''

    def find_last_record(self, key):
        last_key_entry = self.data.rfind(key)

        if last_key_entry > 0:    
            eol            = self.data.find('\n', last_key_entry + 1)
            last_record    = self.data[last_key_entry:eol]
            last_timestamp = self.data[last_key_entry:eol].split()[2]
            return last_record, last_timestamp
        else:
            print('key is not found')
            return -1, -1
        
    def find_all_records(self, key):
        extract = ''
        for record in self.data.splitlines()[:-1]:
            if key == record.split()[0]:
                extract += record + '\n'
        return extract 

    def save(self, new_record):
        key, value, new_timestamp = new_record.split()
        old, t = self.find_last_record(key)
        if t == new_timestamp:
            self.data = self.data.replace(old, new_record)
        else:
            self.data += new_record
        return self.data

    def extract(self, key):
        key = key.strip()
        extract = ''
        if not key:
            pass
        elif key == '*':
            extract = self.data
        else:
            extract = self.find_all_records(key)
        return extract

class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
            
    def data_received(self, data):
        message = data.decode()
        print('Received: ',ascii(message))

        resp = self.process_data(message, storage)

        print('Send: ', ascii(resp))
        self.transport.write(resp.encode())

    def connection_lost(self, exc):
        return super().connection_lost(exc)

    def process_data(self, data, storage):
        err_response = 'error\nwrong command\n\n'

        try:
            #processing empty request like '\n'
            request, payload = data.split(' ',1)
        except ValueError:
            request = payload = data.split()
        
        if request == 'get' and len(data.split()) == 2:
            return 'ok\n' + storage.extract(key=payload) + '\n'

        elif request == 'put' and len(data.split()) == 4:
            value = payload.split()[1]
            timestamp = payload.split()[2]
            
            try:
                value = float(value)
                timestamp = int(timestamp)
            except ValueError:
                print('cannot transform values')
                return err_response
            
            storage.save(new_record=payload)
            return 'ok\n\n'
        else:
            return err_response

storage = Storage()

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