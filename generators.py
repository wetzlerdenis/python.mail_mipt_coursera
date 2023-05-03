###Генераторы - функция, в которой есть оператор yield. Этот оператор
###работает как return, только не прекращает выполнение функции, а лишь прерывает ее на время.
def even_range(start,end):
	current = start
	while current<end:
		yield = current
		current+=2

for number in even_range(0,10):
	print(number)