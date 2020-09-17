'''
Реализовать функцию, принимающую несколько параметров,
описывающих данные пользователя: имя, фамилия, год рождения,
город проживания, email, телефон. Функция должна принимать
параметры как именованные аргументы. Реализовать вывод данных
о пользователе одной строкой.
'''


def my_func(name, surname, year, city, email, phone):
    print(name, surname, year, city, email, phone)

my_func(name='Oleg', surname='Berin', year=1989, city='Moscow', email='mail@mail.ru', phone='555-22-88')