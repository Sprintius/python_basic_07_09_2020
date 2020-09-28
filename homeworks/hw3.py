'''
Создать текстовый файл (не программно), построчно записать
фамилии сотрудников и величину их окладов.
Определить, кто из сотрудников имеет оклад менее 20 тыс.,
вывести фамилии этих сотрудников. Выполнить подсчет средней
величины дохода сотрудников.
'''

def ch_type(type_: type, row: str, pos: int):
    try:
        return type_(list(row.split())[pos])
    except ValueError('Некорректные данные в файле'):
        print('Проверте данные в файле')


try:
    with open('test_3.txt', 'r', encoding='UTF-8') as file:
        many, count, loos = 0, 0, []
        for line in file:
            count += 1
            try:
                many += ch_type(float, line, 1)
                if ch_type(float, line, 1) < 20000:
                    loos.append(ch_type(str, line, 0))
            except TypeError('Некорректные данные в файле'):
                print('Проверте данные в файле')
except (FileNotFoundError, TypeError):
    print('файл не корректный')
print(f'Меньше 20 тыс получают: {loos}\n')
print(f'Средняя величина дохода сотрудников: {(many / count):.2f}')