import threading
import time
from random import randint
from threading import Lock


class Bank:
    lock = Lock()

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self):
        qtd = 100
        while qtd > 0:
            dep = randint(50, 500)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            self.balance += dep
            print(f'Пополнение: {dep}. Баланс: {self.balance}''\n')
            time.sleep(0.001)
            qtd -= 1

    def take(self):
        qtt = 100
        while qtt > 0:
            tk = randint(50, 500)
            print(f'Запрос на {tk}''\n')
            if tk <= self.balance:
                self.balance -= tk
                print(f'Снятие: {tk}. Баланс: {self.balance}''\n')
            else:
                print('Запрос отклонён, недостаточно средств''\n')
                self.lock.acquire()
            time.sleep(0.001)

            qtt -= 1


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')

