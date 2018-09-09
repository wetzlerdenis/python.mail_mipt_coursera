# hometask week 2. Decorator to JSON. 23.12.2017
import json
import functools


def to_json(func):

	@functools.wraps(func)
	def wrapped(*arg, **kwargs):
		result = func(*arg, **kwargs)
		return json.JSONEncoder().encode(result)
	return wrapped
