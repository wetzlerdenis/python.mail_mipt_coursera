#Week 4 task 2
#task 2 description
# Часто при зачислении каких-то средств на счет с нас берут комиссию. 
# Давайте реализуем похожий механизм с помощью дескрипторов. Напишите дескриптор Value, 
# который будет использоваться в нашем классе Account.

# У аккаунта будет атрибут commission. 
# Именно эту коммиссию и нужно вычитать при присваивании значений в amount.

"""
new_account = Account(0.1)
new_account.amount = 100

print(new_account.amount)
90"""

#@staticmethod
#def _calculate_value(value, comm):
#       return value * (1 - comm) 
#я думаю, что надо сделать проверку на то, 
    # что amount не может быть отрицательным 
    # и не может быть текстом 
    # commision can not be taken from negative value

class Value:
    def __init__(self):
        self.value = None
    
    def __get__(self, obj, obj_type): 
        return self.value
    
    def __set__(self, obj, value): 
        print('set = ', value, ', obj=', obj, ' comms = ',obj.commission)
        self.value = value * (1 - obj.commission)

class Account:
    amount = Value() #amount это атрибут класса

    def __init__(self, commission):
        self.commission = commission 
