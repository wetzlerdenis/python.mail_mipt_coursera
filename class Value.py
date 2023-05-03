class Value:
    def __init__(self):
        self.value = None
    
    @staticmethod
    def _prepare_value(value):
        return value * 2

    def __get__(self, obj, obj_type):
        return self.value
    
    def __set__(self, obj, value):
        self.value = self._prepare_value(value)

class Class:
    attr = Value()