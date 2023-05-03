#week 3 task 2
# task description:
#Вам необходимо создать свою иерархию классов для данных, которые описаны в таблице.
#Классы должны называться CarBase (базовый класс для всех типов машин), 
# Car (легковые автомобили), Truck (грузовые автомобили) и SpecMachine (спецтехника). 
# Все объекты имеют обязательные атрибуты:

#- car_type, значение типа объекта и может принимать одно из значений: «car», «truck», «spec_machine».
#- photo_file_name, имя файла с изображением машины, допустимы названия файлов изображений с расширением из списка: «.jpg», «.jpeg», «.png», «.gif»
#- brand, марка производителя машины
#- carrying, грузоподъемность

#В базовом классе CarBase нужно реализовать метод get_photo_file_ext 
# для получения расширения файла изображения. 
#Расширение файла можно получить при помощи os.path.splitext.
#Для грузового автомобиля необходимо в конструкторе класса определить атрибуты: 
# body_length, body_width, body_height, отвечающие соответственно за габариты кузова — 
# длину, ширину и высоту. Габариты передаются в параметре body_whl 
# (строка, в которой размеры разделены латинской буквой «x»). 
# Обратите внимание на то, что характеристики кузова должны быть вещественными 
# числами и характеристики кузова могут быть не валидными (например, пустая строка).
# В таком случае всем атрибутам, отвечающим за габариты кузова, 
# присваивается значение равное нулю.
#Также для класса грузового автомобиля необходимо реализовать метод 
# get_body_volume, возвращающий объем кузова.
#В классе Car должен быть определен атрибут passenger_seats_count 
# (количество пассажирских мест), а в классе SpecMachine — extra 
# (дополнительное описание машины).
#Полная информация о атрибутах классов приведена в таблице ниже, 
# где 1 - означает, что атрибут обязателен для объекта, 
# 0 - атрибут должен отсутствовать.

import csv
import os
class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        try:
            ext = photo_file_name.split( sep = '.')[1]
            filename = photo_file_name.split( sep = '.')[0]
        except IndexError:
            raise
        if len(photo_file_name.split( sep = '.')) != 2:
            raise ValueError
        if brand == '' or \
            photo_file_name == '' or \
            carrying == '' or\
            filename == '':
            raise ValueError
        elif ext == 'jpg' or \
            ext == 'jpeg' or \
            ext == 'png' or \
            ext == 'gif':
            self.brand = brand
            self.photo_file_name = photo_file_name
            self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name,carrying)
        self.car_type = 'car'
        if passenger_seats_count == '':
            raise ValueError
        else:
            self.passenger_seats_count = int(passenger_seats_count)

class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name,carrying)
        self.car_type = 'truck'
        
        try:
            whl = body_whl.split(sep='x')
            if len(whl) != 3:
                raise ValueError
            self.body_length = float(whl[0])
            self.body_width = float(whl[1])
            self.body_height = float(whl[2])
        except ValueError:
            self.body_length,self.body_width,self.body_height = 0.0,0.0,0.0
            
    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

class SpecMachine(CarBase):
    
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name,carrying)
        self.car_type = 'spec_machine'
        if extra == '':
            raise ValueError
        else:
            self.extra = extra

        
def get_car_list(csv_filename):
    car_list = []
    
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            print(row)
            try:
                cartype = row[0]
            except IndexError: 
                continue
                
            if cartype == 'car':
                try:
                    car_list.append(Car(row[1],row[3],row[5],row[2]))
                except (IndexError, ValueError): 
                    continue
                    
            if cartype == 'truck':
                try:
                    car_list.append(Truck(row[1],row[3],row[5],row[4]))
                except (IndexError, ValueError): 
                    continue
                    
            if cartype == 'spec_machine':
                try:
                    car_list.append(SpecMachine(row[1],row[3],row[5],row[6]))
                except (IndexError, ValueError):
                    continue
            
    return car_list