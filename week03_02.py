import csv
class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name,carrying)
        self.car_type = 'car'
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name,carrying)
        self.car_type = 'truck'
        
        if body_whl:
            whl = body_whl.split(sep='x')
            self.body_length = float(whl[0])
            self.body_width = float(whl[1])
            self.body_height = float(whl[2])
        else: 
            self.body_length,self.body_width,self.body_height = 0,0,0
            
    def get_body_volume(self):
        return self.body_length*self.body_width*self.body_height

class SpecMachine(CarBase):
    
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name,carrying)
        self.car_type = 'spec_machine'
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
                except IndexError: 
                    continue
                    
            if cartype == 'truck':
                try:
                    car_list.append(Truck(row[1],row[3],row[5],row[4]))
                except IndexError: 
                    continue
                    
            if cartype == 'spec_machine':
                try:
                    car_list.append(SpecMachine(row[1],row[3],row[5],row[6]))
                except IndexError:
                    continue
            
    return car_list
