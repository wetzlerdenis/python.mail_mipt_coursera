#Week 4 task 2
#task 2 description
# Часто при зачислении каких-то средств на счет с нас берут комиссию. 
# Давайте реализуем похожий механизм с помощью дескрипторов. Напишите дескриптор Value, 
# который будет использоваться в нашем классе Account.


#я думаю, что надо сделать проверку на то, 
# что amount не может быть отрицательным 
# и не может быть текстом 
# commision can not be taken from negative value

class Account:
    amount = Value() #amount это атрибут класса

    def __init__(self, commission):
        self.commission = commission 

# У аккаунта будет атрибут commission. 
# Именно эту коммиссию и нужно вычитать при присваивании значений в amount.

"""
new_account = Account(0.1)
new_account.amount = 100

print(new_account.amount)
90"""

if __name__ == "__main__":

    new_account = Account(0.02)

#в атрибут new_account.commision записалось значение 0.1
    new_account.amount = 100
    print(new_account.amount)

#90
# Опишите дескриптор в файле и загрузите его на платформу.