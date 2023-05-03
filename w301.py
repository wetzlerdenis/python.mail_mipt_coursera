#Week 3 task 1
#Task description:
# Первое задание на этой неделе — не сложное, для разогрева. 
# Ваша задача: написать python-модуль solution.py, внутрь которого необходимо 
# поместить код класса FileReader. 
# Конструктор этого класса принимает один параметр: путь до файла на диске. 
# В классе FileReader должен быть реализован метод read, возвращающий строку - 
# содержимое файла, путь к которому был указан при создании экземпляра класса. 
# Python модуль должен быть написан таким образом, чтобы импорт класса FileReader 
# из него не вызвал ошибок.
# При написании реализации метода read, вам нужно учитывать случай, 
# когда при инициализации был передан путь к несуществующему файлу. 
# Требуется обработать возникающее при этом исключение FileNotFoundError 
# и вернуть из метода read пустую строку.

  
class FileReader(object):
	"""docstring for FileReader"""
	def __init__(self, path):
		self.path = path

	def read(self):
		"""Return the file's content as a line"""
		try:
			with open(self.path,'r') as f:
				read_data = f.read()
			return read_data
		
		except (IOError, OSError):
			return ""

# def _main():
# 	example = FileReader("city.py")
# 	print(example.read())

# if __name__ == '__main__':
# 	_main()