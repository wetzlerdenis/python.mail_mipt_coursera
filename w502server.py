# !/usr/bin/env python
# -*- coding: utf-8 -*-
#реализация сервера для тестирования метода get по заданию - Клиент для отправки метрик

import socket

sock = socket.socket()
sock.bind(('127.0.0.1', 8889))
sock.listen(1)
conn, addr = sock.accept()

print('Соединение установлено:', addr)

# переменная response хранит строку возвращаемую сервером, если вам для
# тестирования клиента необходим другой ответ, измените ее
response = b'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'
response_empty = b'ok\n\n'

while True:
    data = conn.recv(1024)
    if not data:
        break
    request = data.decode('utf-8')
    print(f'Получен запрос:{ascii(request)}')

    if request == 'get palm.cpu\n':
        print(f'Отправлен ответ {ascii(response.decode("utf-8"))}')
        conn.send(response)
    elif request == 'get xxx\n':
        break
    else:
        print(f'Отправлен ответ {ascii(response_empty.decode("utf-8"))}')
        conn.send(response_empty)

conn.close()
sock.close()