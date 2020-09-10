"""
Задание№1. Поработайте с переменными, создайте несколько,
выведите на экран, запросите у пользователя несколько чисел и
строк и сохраните в переменные, выведите на экран.
"""

ask_name = input("Ваше имя \n")
ask_surname = input("Ваша фамилия \n")
ask_age = input("Ваш возраст \n")
ask_weight = input("Ваш вес \n")

print(ask_name, ask_surname, ask_age, ask_weight, sep=',')

""""
2. Пользователь вводит время в секундах. Переведите
время в часы, минуты и секунды и выведите в формате чч:мм:сс.
Используйте форматирование строк.
"""

time = int(input("Введите время в секундах \n"))

hours = time // 3600
minutes = (time % 3600) // 60
seconds = (time % 3600) % 60


print(f"Время в формате чч:мм:сс -  {hours} : {minutes} : {seconds}")

"""
3. Узнайте у пользователя число n. Найдите сумму чисел n + nn + nnn.
Например, пользователь ввёл число 3. Считаем 3 + 33 + 333 = 369.
"""

n = int(input("Введите число \n"))

total = (n + int(str(n) + str(n)) + int(str(n) + str(n)+ str(n)))
print("Сумма чисел n + nn + nnn - %d" % total)

"""
4. Пользователь вводит целое положительное число.
Найдите самую большую цифру в числе. Для решения
используйте цикл while и арифметические операции.
"""


i = 3481561
r = -1
while i > 0:
    d = i % 10
    i //= 10
    if d > r:
        r = d
print(r)

"""
5. Запросите у пользователя значения выручки и издержек фирмы.
Определите, с каким финансовым результатом работает фирма
(прибыль — выручка больше издержек, или убыток — издержки
больше выручки). Выведите соответствующее сообщение. Если
фирма отработала с прибылью, вычислите рентабельность выручки
(соотношение прибыли к выручке). Далее запросите численность
сотрудников фирмы и определите прибыль фирмы в расчете на одного сотрудника.
"""

profit = int(input("Введите выручку фирмы в руб. \n"))
costs = int(input("Введите издержки фирмы в руб. \n"))
if profit > costs:
    print(f"Фирма работает с прибылью. Рентабельность выручки {profit / costs:.2f}")
    workers = int(input("Введите количество сотрудников фирмы \n"))
    print(f"Прибыль на одного сторудника составила {(profit - costs) / workers:.2f}")
elif profit == costs:
    print("Фирма работает в ноль")
else:
    print("Фирма работает в убыток")

'''
6. Спортсмен занимается ежедневными пробежками. В первый
день его результат составил a километров. Каждый день
спортсмен увеличивал результат на 10 % относительно предыдущего.
Требуется определить номер дня, на который общий результат спортсмена
 составить не менее b километров. Программа должна принимать
 значения параметров a и b и выводить одно натуральное число — номер дня.
'''

a = int(input("Введите результат пробежки первого дня \n"))
b = int(input("Введите желаемый результат пробежки в км \n"))
days = 1
distance = a
while distance < b:
        a = a * 1.1
        days = days + 1
        distance = distance + a
print(f"Вы достигнете требуемых показателей на %.d день" % days)