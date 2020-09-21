'''
Реализовать скрипт, в котором должна быть предусмотрена
 функция расчета заработной платы сотрудника. В расчете
 необходимо использовать формулу:
 (выработка в часах*ставка в час) + премия.
 Для выполнения расчета для конкретных значений необходимо
 запускать скрипт с параметрами.
'''

from sys import argv

name, worked_time, price_per_hour, bonus = argv
try:
    worked_time = int(worked_time)
    price_per_hour = int(price_per_hour)
    bonus = int(bonus)
    res = worked_time * price_per_hour + bonus
    print(f'Заработная плата сотрудника  {res}')
except ValueError:
    print('Not a number')