"""
Создать (программно) текстовый файл, записать в него программно набор чисел, разделенных пробелами.
Программа должна подсчитывать сумму чисел в файле и выводить ее на экран.
"""

import random

random.seed()

f_name = "test_5.txt"
with open(f_name, "w") as f:
    for _ in range(random.randint(10, 20)):
        print(random.randint(0, 100), end=" ", file=f)
with open(f_name, "r") as ff:
    data = ff.read().rstrip(" ")
    nums = data.split(" ")
    s = 0
    for n in nums:
        s += int(n)
    print(f'Nums: {", ".join(nums)}')
    print(f'Sum = {s}')