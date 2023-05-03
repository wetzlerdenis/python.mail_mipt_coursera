import argparse
import os
import tempfile
import json

storage = argparse.ArgumentParser()
storage.add_argument("--key", help="input key's name",required=True)
storage.add_argument("--val", help="value of key", default=None)
args = storage.parse_args()
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

data_base = None

if os.path.exists(storage_path): 
	with open(storage_path,'r') as f:
		data_base = json.load(f)
		
if data_base is None:
	data_base = {}
	with open(storage_path,'w') as f:
		json.dump(data_base, f)

sentinel = object()
if data_base.get(args.key, sentinel) == sentinel: #если ключ не найден
	if args.val is not None: # и если было значение --val smth
		data_base[args.key] = [args.val] # добавь эту пару в словарь
		with open(storage_path, 'w') as f:
			json.dump(data_base, f)

	else: # если значения --val не было
		print(None)
else: 
#если ключ найден, вообще говоря функция вернет value по этому ключу
	if args.val is not None: # и если было значение --val smth
		#if args.val not in data_base[args.key]: # если такого val нет в списке values_list
			data_base[args.key].append(args.val) # добавь в лист с остальными
			with open(storage_path, 'w') as f:
				json.dump(data_base, f)
	else:
		#если --val smth None, выведи все ключи через запятую, нет проверки на порядок добавления
		print(', '.join(data_base[args.key]))