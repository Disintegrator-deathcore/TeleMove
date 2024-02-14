import random
import os
from progress.bar import IncrementalBar

path = input("Введите путь до папки в которой нужно создать множество файлов: ")
#path = "C:\\programming\\python\\TeleMove\\TestFolder"
file_types = ['exe', 'dll', 'psd', 'vdf', 'txt', 'doc', 'docx', 'mp4']
alph = []

for i in range(ord("а"), ord("я")):
    alph.append(chr(i))

bar = IncrementalBar("Создаём множество файлов: ", max=1_000)
for i in range(1_000):
    for i in range(random.randint(20, 50)):
        filename = ""
        for j in range(10):
            filename += (alph[random.randint(0, len(alph))-1])
        filename = filename + "." + (file_types[random.randint(0, len(file_types))-1])

        full_name = path + "\\" + filename
        f = open(full_name, "w")
        for symb in range(random.randint(0, 10_000)):
            f.write(alph[0])
        f.close
    bar.next()
print()
print("Множество файлов создано")
input("Нажмите Enter")