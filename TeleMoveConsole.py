import os
from progress.bar import IncrementalBar
import shutil


# Функция получения файлов из папки
def read_folder(path):
    all_files = os.listdir(path)
    files = []

    bar = IncrementalBar('Получаем файлы из папки: ', max=len(all_files))

    for file in all_files:
        full_path = path + "\\" + file

        if os.path.isfile(full_path):
            files.append(file)
        bar.next()
    print()
    print()

    return files


# Функция создания дерева папок
def make_folders_tree(sort_type, files, file_extensions, path):
    if sort_type == "1":
        sort_by_name(files, path)
    elif sort_type == "2":
        sort_by_file_extension(files, file_extensions, path)
    elif sort_type == "3":
        sort_by_file_size(files, path)
    # elif sort_type == "4":
    #     sort_by_filetype(files, path)


# Функция сортировки файлов по их расширениям        
def sort_by_file_extension(files, file_extensions, path):
    try:
        bar = IncrementalBar("Создаём папки: ", max=len(file_extensions))
        for file_extension in file_extensions:
            os.mkdir(path + "\\" + file_extension)
            bar.next()
        print()
        print()
    except FileExistsError:
        print("папка существует")

    dirs = []
    all_el = os.listdir(path)
    print("Отделяем файлы от папок")
    print()

    for directory in all_el:
        if (not (os.path.isfile(path + "\\" + directory))) and (directory in file_extensions):
            dirs.append(directory)
        if len(dirs) == len(file_extensions):
            break
    print()
    print()
    
    bar = IncrementalBar("Распихиваем по папкам: ", max=len(dirs))    
    for directory in dirs:
        for file in files:
            if directory == file.split(".")[-1]:
                shutil.move(path + "\\" + file, (path + "\\" + directory))
        bar.next()
    print()
    print()


# Сортировка файлов по их наименованию
def sort_by_name(files, path):
    alph = []

    bar = IncrementalBar("Получаем первые буквы файлов: ", max=len(files))
    for file in files:
        if file[0].upper() not in alph:
            alph.append(file[0].upper())
        bar.next()
    print()
    print()

    try:
        bar = IncrementalBar("Создаём папки: ", max=len(alph))
        for symbol in alph:
            os.mkdir(path + "\\" + symbol)
            bar.next()
        print()
        print()
    except FileExistsError:
        print("папка существует")

    dirs = []

    print("Отделяем файлы от папок")
    print()
    for directory in os.listdir(path):
        if (not (os.path.isfile(path + "\\" + directory))) and (directory in alph):
            dirs.append(directory)
        if len(dirs) == len(alph):
            break
    
    bar = IncrementalBar("Распихиваем по папкам: ", max=len(dirs))    
    for directory in dirs:
        for file in files:
            if directory == file[0].upper():
                shutil.move((path + "\\" + file), (path + "\\" + directory))
        bar.next()
    print()
    print()


# Функция получения расширений файлов
def get_files_extensions(files):
    file_extensions = []

    bar = IncrementalBar("Получаем расширения файлов: ", max=len(files))

    for file in files:
        file_extension = file.split(".")[-1]

        if file_extension not in file_extensions:
            file_extensions.append(file_extension)
        bar.next()
    print()
    print()

    return file_extensions


# Функция сортировки файлов по размеру
def sort_by_file_size(files, path):
    while True:
        sort_size = input("Введите число в килобайтах: ")

        if not sort_size.isdigit():
            print("Число должно состоять только из цифр больше нуля")
            print("Попробуйте ещё раз")
            print()
        elif int(sort_size) <= 0:
            print("Число должно состоять только из цифр больше нуля")
            print("Попробуйте ещё раз")
            print()
        else:
            break
    print()
        
    sort_size = int(sort_size)
    
    all_sizes = []

    bar = IncrementalBar("Получаем размеры файлов: ", max=len(files))
    for file in files:
        if int((os.path.getsize(path + "\\" + file)/1024)+0.5) not in all_sizes:
            all_sizes.append(int(os.path.getsize(path + "\\" + file)/1024+0.5))
        bar.next()
    print()
    print()

    all_sizes.sort()
    needed_sizes = []

    for file_size in all_sizes:
        if file_size % sort_size == 0 and file_size != 0:
            needed_sizes.append(file_size)
        elif all_sizes[all_sizes.index(file_size)] == all_sizes[-1]:
            needed_sizes.append(file_size)

    try:
        bar = IncrementalBar("Создаём папки: ", max=len(needed_sizes))
        for f_size in needed_sizes:
            if f_size - sort_size != 0:
                os.mkdir(path + "\\" + str(str(f_size-sort_size+1) + "-" + str(f_size)))
            else:
                os.mkdir(path + "\\" + str(str(f_size-sort_size) + "-" + str(f_size)))
            bar.next()
        print()
        print()
    except FileExistsError:
        print("папка существует")

    dirs = []

    print("Отделяем файлы от папок")
    print()
    for directory in os.listdir(path):
        if (not (os.path.isfile(path + "\\" + directory))) and (int(directory.split("-")[-1]) in needed_sizes):
            dirs.append(int(directory.split("-")[-1]))
        if len(dirs) == len(needed_sizes):
            break
    
    bar = IncrementalBar("Распихиваем по папкам: ", max=len(dirs))
    dirs.sort()

    for directory in dirs:
        for file in files:
            try:
                if ((directory+0.5 >= int(os.path.getsize(path + "\\" + file)) / 1024 + 0.5) and
                        (int(directory) - sort_size != 0)):
                    shutil.move((path + "\\" + file),
                                (path + "\\" + str(str(directory-sort_size+1) + "-" + str(directory))))
                elif ((directory+0.5 >= int(os.path.getsize(path + "\\" + file)) / 1024 + 0.5) and
                      (int(directory) - sort_size == 0)):
                    shutil.move((path + "\\" + file),
                                (path + "\\" + str(str(directory-sort_size) + "-" + str(directory))))
            except FileNotFoundError:
                pass
        bar.next()
    print()
    print()


# # Функция сортировки файлов по типу
# def sort_by_filetype(files, path):
#     try:
#         bar = IncrementalBar("Создаём папки: ", max=len(file_extensions))
#         for file_extension in file_extensions:
#             os.mkdir(path + "\\" + file_extension)
#             bar.next()
#         print()
#         print()
#     except FileExistsError:
#         print("папка существует") 


# Назначение пути
path = input("Введите путь до директории: ")
# path = "C:\\programming\\python\\TeleMove\\TestFolder"
print(f"Путь к папке: {path}")

# Выбор типа сортировки
sort_type = ""
while True:
    print("Выберите тип сортировки: ")
    print("1. По алфавиту\t2. По типу\t3. По размеру")
    sort_type = input()

    if not sort_type.isdigit():
        print("При выборе типа сортировки необходимо писать число, попробуйте ещё раз.")
    
    elif int(sort_type) <= 0 or int(sort_type) > 3:
        print("Данного выбора нет в списке, попробуйте ещё раз")
    
    else:
        break

# Нахождение файлов в директории и получение их типов
files = read_folder(path)

if sort_type == "2":
    file_extensions = get_files_extensions(files)
else:
    file_extensions = ""

make_folders_tree(sort_type, files, file_extensions, path)

print("Завершено, нажмите Enter")
input()
