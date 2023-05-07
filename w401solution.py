#week 4 Magic methods, iterators, context managers
#task 1 description
# В этом задании вам нужно создать интерфейс для работы с файлами. 
# Интерфейс должен предоставлять следующие возможности по работе с файлами:
#
# 1) чтение из файла, метод read возвращает строку с текущим содержанием файла
# 2) запись в файл, метод write принимает в качестве аргумента строку с новым содержанием файла
# 3) сложение объектов типа File, результатом сложения является объект класса File, 
#  при этом создается новый файл и файловый объект, в котором содержимое второго файла 
#  добавляется к содержимому первого файла. Новый файл должен создаваться в директории, 
#  полученной с помощью функции tempfile.gettempdir. 
#  Для получения нового пути можно использовать os.path.join.
# 4) возвращать в качестве строкового представления объекта класса File полный путь до файла
# 5) поддерживать протокол итерации, причем итерация проходит по строкам файла

# При создании экземпляра класса File в конструктор передается полный путь до файла на файловой системе. 
# Если файла с таким путем не существует, он должен быть создан при инициализации.

#Пример работы:

import os.path
# from solution import File
# path_to_file = 'some_filename'
# os.path.exists(path_to_file)
# False

#file_obj = File(path_to_file)
#os.path.exists(path_to_file)
# True

#file_obj.read()
#''
class File():
    
    def __init__(self, filepath):
        self.filepath = filepath
        try: 
            file = open(filepath, 'x')
        except Exception:
            pass

    def path_validation():
        "Если путь к файлу неправильный"
        pass

    def __str__(self):
        # 4) возвращать в качестве строкового представления 
        # объекта класса File полный путь до файла
        pass

    def __add__ (self, obj):
        pass

    def read(self):
        # 1) чтение из файла, метод read возвращает строку 
        # с текущим содержанием файла
        with open(self.filepath, 'r') as f:
            return f.read()

    def write(new_text):
        # 2) запись в файл, метод write принимает в качестве 
        # аргумента строку с новым содержанием файла
        pass

    
