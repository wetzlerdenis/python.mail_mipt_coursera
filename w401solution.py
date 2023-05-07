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
import tempfile

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
        """возвращать в качестве строкового представления 
        объекта класса File полный путь до файла"""
        
        return os.path.abspath(self.filepath)

    def __add__ (self, obj):
        """сложение объектов типа File, результатом сложения 
        является объект класса File, при этом создается новый 
        файл и файловый объект, в котором содержимое второго файла 
        добавляется к содержимому первого файла"""

        temp_dir = tempfile.gettempdir()
        temp_file_name = next(tempfile._get_candidate_names())
        temp_file_path = os.path.join(temp_dir, temp_file_name)
        
        new_obj = File(temp_file_path)
        added_text = self.read() + obj.read()
        new_obj.write(added_text)
        
        return new_obj 

    def __iter__(self):
        with open(self.filepath) as f:
            lines = f.readlines()
        self.line_index = 0
        return self
    
    def __next__(self):
        if self.line_index < len(self.lines):
            line = self.lines[self.line_index]
            self.line_index += 1
        else:
            raise StopIteration
        return line

    def read(self):
        """чтение из файла, метод read возвращает строку 
         с текущим содержанием файла"""
        
        with open(self.filepath, 'r') as f:
            return f.read()

    def write(self, new_text):
        """запись в файл, метод write принимает в качестве 
        # аргумента строку с новым содержанием файла"""

        with open(self.filepath, 'w') as f:
            return f.write(new_text)

    
