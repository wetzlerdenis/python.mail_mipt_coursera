#week5
#Task 1 Client for work with metrics

"""Реализация клиента.
Необходимо реализовать класс Client, в котором будет инкапсулировано соединение 
с сервером, клиентский сокет и методы для получения (get) и отправки (put) метрик на сервер. 

В конструктор класса Client должна передаваться адресная пара хост и порт, 
а также необязательный аргумент timeout (по умолчанию - None). 
Соединение с сервером устанавливается при создании экземпляра класса Client 
и не должно разрываться между запросами:
client = Client("127.0.0.1", 8888, timeout=15)

Необходимо предоставить модуль с реализованным классом Client, пользовательским 
исключением ClientError. 

При вызове методов get и put клиент должен 
- посылать сообщения в TCP-соединение с сервером
- получать ответ от сервера и 
- возвращать словарь с данными

Клиент должен быть синхронным

Протокол Клиент посылает Серверу 2 вида запросов:
- отправка данных для сохранения их на сервере
- получения сохраненных данных

Client          -->     Server

get <metric>\n  -->     Server
put <data>\n    -->     Server
Client          <--     ok\n<response>\n\n
Client          <--     error\n<response>\n\n

Examples:

Метод put принимает в качестве параметров: 
    - название метрики, 
    - численное значение 
    - необязательный параметр timestamp

Если метод put вызван без timestamp, то клиент должен подставить временную отметку, 
полученную с помощью вызова int(time.time())

put palm.cpu 23.7 1150\n    -->     Server
Client                      <--     ok\n\n

put palm.cpu 23.7\n         -->     Server
Client                      <--     ok\n\n

put <value> и <timestamp> не преобразуются к float и int
Client                      <--     error\nwrong command\n\n

Метод put не возвращает ничего в случае успешной отправки и выбрасывает 
пользовательское исключение ClientError в случае не успешной.


Метод get принимает в качестве параметра имя метрики или символ «*»
Метод get возвращает словарь с метриками в случае успешного получения
ответа от сервера и выбрасывает исключение ClientError в случае не успешного.

Клиент получает данные от сервера в текстовом виде, метод get должен обработать 
строку ответа и вернуть словарь с полученными ключами с сервера. Значением 
ключей в словаре является список кортежей:
[(timestamp1, metric_value1), (timestamp2, metric_value2), …]

Значение timestamp и metric_value должны быть преобразованы соответственно 
к типам int и float. Список должен быть отсортирован по значению timestamp 
(по возрастанию).

Пример возвращаемого значения при успешном вызове client.get("palm.cpu"):

{
    'palm.cpu': [
        (1150864247, 0.5),
        (1150864248, 0.5)
        ]
}
Если в ответ на get-запрос сервер вернул положительный ответ "ok\n\n", 
но без данных, то метод get клиента должен вернуть пустой словарь.

get palm.cpu\n  -->     Server
Client          <--     ok\npalm.cpu 2.0 1150\npalm.cpu 0.5 1150\n\n

get *\n         -->     Server
Client          <--     ok\npalm.cpu 2.0 1150\npalm.cpu 0.5 1150\neardrum.cpu 3.0 1150\n\n

get <unknown metric>        -->     Server
Client                      <--     ok\n\n

get нарушен формат запроса  -->     Server
Client                      <--     error\nwrong command\n\n

get ошибочная команда       -->     Server
Client                      <--     error\nwrong command\n\n

print(client.get("*"))
"""
import socket
import time

class ClientError(Exception):
    pass

class Client():

    def __init__(self, address, port, timeout=None):
        """
        Example: client = Client("127.0.0.1", 8888, timeout=15)
        """
        self.address = address
        self.port = port
        self.timeout = timeout
        try:
            self.sock = socket.create_connection((address, port), self.timeout)
        except socket.error as err:
            raise ClientError

    def put(self, metric, value, timestamp=None):
        
        if not timestamp:
            timestamp = int(time.time())

        data = f"put {metric} {value} {timestamp}\n"
        
        try:
            self.sock.sendall(data.encode('utf8'))
        except (socket.error, socket.timeout) as e:
            raise ClientError
        
        try:
            server_response = self.sock.recv(1024).decode('utf-8')
            
            if not server_response:
                raise ClientError
            
            if server_response.startswith('error'):
                raise ClientError
            
        except socket.error:
            raise ClientError
        
    def get(self, metric):
        
        data = f"get {metric}\n"

        try:
            self.sock.sendall(data.encode('utf8'))
        except (socket.error, socket.timeout) as e:
            raise ClientError
        
        try:
            server_response = self.sock.recv(1024).decode('utf-8')
            
            if not server_response:
                raise ClientError
            else:
                return server_response
            
        except socket.error as e:
            raise ClientError
        
        self.sock.close()

        #TODO: проверить формат запроса на правильность, а именно наличие
        # символа окончания строки \n в конце реквеста без пробела

        #TODO: Проверить тело запроса, что оно не состоить из одного символа
        # переноса строки