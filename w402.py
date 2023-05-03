#Week 4 task 2
#task 2 description
# Часто при зачислении каких-то средств на счет с нас берут комиссию. 
# Давайте реализуем похожий механизм с помощью дескрипторов. Напишите дескриптор Value, 
# который будет использоваться в нашем классе Account.

class Value:
    #я думаю, что надо сделать проверку на то, 
    # что amount не может быть отрицательным 
    # и не может быть текстом 
    # commision can not be taken from negative value

    def __init__(self):
        self.value = None
    
    @staticmethod
    def _calculate_value(value, comm):
        return value * (1 - comm) 

    def __get__(self, obj, obj_type): 
        return self.value
    
    def __set__(self, obj, value): 
        self.value = self._calculate_value(value, obj.commission)

class Account:
    amount = Value() #amount это атрибут класса

    def __init__(self, commission):
        self.commission = commission 

# У аккаунта будет атрибут commission. 
# Именно эту коммиссию и нужно вычитать при присваивании значений в amount.
if __name__ == "__main__":

    new_account = Account(0.02)

#в атрибут new_account.commision записалось значение 0.1
    new_account.amount = 100
    print(new_account.amount)

#90
# Опишите дескриптор в файле и загрузите его на платформу.