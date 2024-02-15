from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ

# Задание 1. Распределяем ФИО по столбцам.
lfs_list = []
for i in contacts_list:
    lfs = i[0] + ' ' + i[1] + ' ' + i[2]
    lfs_list.append(lfs.strip())

split_lfs_list = []
for i in lfs_list:
    split_lfs_list.append(i.split())

for index, cont in enumerate(contacts_list):

    cont[0] = split_lfs_list[index][0]    
    cont[1] = split_lfs_list[index][1]
    if len(split_lfs_list[index]) == 2:
        cont[2] = ''
    elif len(split_lfs_list[index]) == 3:
        cont[2] = split_lfs_list[index][2]
   
# pprint(contacts_list)
        
# Задание 2. Форматируем телефоны по заданному образцу.
for t in contacts_list[1:]:
    tel = t[5]
    if '(' in tel and 'доб' not in tel:
        pattern_cmp = re.compile(r'(\+7|8)(\s*(\(?\d+\))\s*(\d+)[- ](\d+)[- ](\d+))')
        result_tel = pattern_cmp.sub(r'+7\3\4-\5-\6', tel)
        t[5] = result_tel

    elif 'доб' in tel:
        pattern_cmp = re.compile(r'(\+7|8)(\s*(\(?\d+\))\s*(\d+)[- ](\d+)[- ](\d+))\s\(*(доб.)\s(\d+)\)*')
        result_tel = pattern_cmp.sub(r'+7\3\4-\5-\6 \7\8', tel)
        t[5] = result_tel

    elif '(' not in tel:
        pattern_cmp = re.compile(r'(\+7|8)\s*(\d{3})[- ]*(\d{3})[- ]*(\d{2})(\d{2})')
        result_tel = pattern_cmp.sub(r'+7(\2)\3-\4-\5', tel)
        t[5] = result_tel
contacts_list.sort()
# pprint(contacts_list)

# Задание 3. Соединяем повторяющиеся контакты.

new_contact_list = []
for index, contact in enumerate(contacts_list):
# Сначала добавляем в new_contact_list повторяющиеся контакты и объединяем их.
    if contact[0] == contacts_list[index - 1][0] and contact[1] == contacts_list[index - 1][1]:
        new_contact = []
        for i in range(len(contact)):
            element = max([contact[i], contacts_list[index - 1][i]])
            new_contact.append(element)
        new_contact_list.append(new_contact)
 
# Теперь добавляем в new_contact_list те контакты, которые встречаются только один раз.
def contact_exists(contact, contact_list):
    for cont in contact_list:
        if contact[0] == cont[0] and contact[1] == cont[1]:
           return True

for old_contact in contacts_list:
    if not contact_exists(old_contact, new_contact_list):
        new_contact_list.append(old_contact)
    
new_contact_list.sort()   
pprint(new_contact_list)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("new_phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',', lineterminator='\n')
    datawriter.writerows(new_contact_list)
    