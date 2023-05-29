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

stor = ''

def find_last_record(key):
    last_key_entry = stor.rfind(key)

    if last_key_entry > 0:    
        eol            = stor.find('\n', last_key_entry + 1)
        last_record    = stor[last_key_entry:eol]
        last_timestamp = stor[last_key_entry:eol].split()[2]
        print('last record found: ', last_record)
        return last_record, last_timestamp
    else:
        print('key is not found')
        return -1, -1

def find_all_records(key):
    extract = ''
    print('starting looking into stor: ', stor)
    for record in stor.splitlines()[:-1]:
        if key == record.split()[0]:
            print('key is found in stor, extracting...')
            extract += record + '\n'
            print('extract added')
    
    print('finally ready to extract: ', extract)
    return extract 

def save(new_record):
    key, value, new_timestamp = new_record.split()
    old, t = find_last_record(key)
    if t == new_timestamp:
        print('replacing record...')
        stor = stor.replace(old, new_record)
    else:
        try:
            print('trying to add new record...')
            stor += new_record
            print('saved new record, stor:', stor)
        except NameError:
            print('stor was not created')
    return stor

def extract(key):
    key = key.strip()
    # extract = ''
    if not key:
        pass
    elif key == '*':
        return stor
    else:
        return find_all_records(key)
    # return extract

def better_process_data(data):
    err_response = 'error\nwrong command\n\n'
    ok_response = 'ok\n\n'

    try:
        #processing empty request like '\n'
        request, payload = data.split(' ',1)
    except ValueError:
        request = payload = data.split()
    
    if request == 'get' and len(data.split()) == 2:
        return 'ok\n' + extract(payload) + '\n'
    
    elif request == 'put' and len(data.split()) == 4:
        value = payload.split()[1]
        timestamp = payload.split()[2]
        
        try:
            value = float(value)
            timestamp = int(timestamp)
        except ValueError:
            print('cannot transform values')
            return err_response
        
        save(payload)
        return ok_response
    else:
        return err_response
    

class ClientServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
            
    def data_received(self, data):
        message = data.decode()
        print('Received: ',ascii(message))

        # resp = self.process_data(message, stor)
        resp = better_process_data(message)

        print('Send: ', ascii(resp))
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