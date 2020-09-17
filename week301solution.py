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

