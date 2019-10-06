import mimetypes
import os
import random
from django.http import HttpResponse
from docxtpl import DocxTemplate
from Helper.change_word import *

GenderMass = ["студентки", "студента"]
ConcessionMass = ["студент-сирота", "cтудент-инвалид", "cтудент, имеющий детей", "cтудент из многодетной семьи", "cтудент-участник военных действий", "cтудент-чернобылец", "cтудент, имеющий родителей-инвалидов, родителей-пенсионеров", "cтудент из неполной семьи", "cтудент из малоимущей семьи", "cтудент, находящийся на диспансерном учёте с хроническими заболеваниями", "студент, проживающий в общежитии"]

# Выбор зам декана по курсу
def chooseDirector(group):
    director = group[4]
    director = {
        '1': "Н.В. Попова",
        '2': "И.А. Коновал",
        '3': "Т.В. Гаранина",
        '4': "Е.В. Бычкова",
        '5': "Н.Ю. Лахметкина",
    }.get(director, 0)
    return director

# Функкция создания ворд документа по шаблону
def CreateWord(gender, group, surname, name, lastname, number, typeconcession, chooseDoc):
    # Проверка на пустоту
    if gender is None or group is None or surname is None or name is None or lastname is None or number is None or typeconcession is None:
        return "Error NoData"
    # Проверка наличия данных
    if gender == '' or group == '' or surname == '' or name == '' or lastname == '' or number == '' or typeconcession == '':
        return "Error NoData"
    # Проверка длинны полученных данных, ограничение 128 символов
    if len(group) > 128 or len(group) > 128 or len(group) > 128 or len(group) > 128 or len(group) > 128 or len(
            group) > 128:
        return "Error Len"

    # Проверка полученного пола, и перевод его в текст
    if gender != "1" and gender != "0":
        return "Error Gender"
    gender = GenderMass[int(gender)]

    # Задание параметров для шаблона и сохранение результата
    random.seed()
    if chooseDoc == '1':
        #doc = DocxTemplate("template1.docx")
        # ДЛЯ REG RU
        doc = DocxTemplate("Helper/template1.docx")
    elif chooseDoc == '2':
        #doc = DocxTemplate("template2.docx")
        # ДЛЯ REG RU
        doc = DocxTemplate("Helper/template2.docx")
        typeconcession = 10
    else:
        print("chooseDoc error")
        return "Error no chooseDoc"

    if int(typeconcession) < 0 or int(typeconcession) > 10:
        return "Error typeConcession"

    typeconcession = ConcessionMass[int(typeconcession)]

    director = chooseDirector(group)

    context = {'gender': gender,
               'group': group,
               'surname': Genitive_SecondName(surname, lastname),
               'name': Genitive_Name(name, lastname),
               'lastname': Genitive_MiddleName(lastname),
               'number': number,
               'typeconcession': typeconcession,
               'director': director}

    doc.render(context)
    LogFile = True
    File_Path = ""
    while LogFile:
        try:
            File_Path = "temp" + str(random.randint(1, 10000)) + ".docx"
            file = open(File_Path)
            file.close()
        except IOError as e:
            break

    # Формирование ответа для пользователя
    doc.save(File_Path)
    File_Path = os.path.abspath(File_Path)
    fp = open(File_Path, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(File_Path)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(File_Path).st_size)
    response['Content-Disposition'] = "attachment; filename=Zaiavlenui_Na_matpomosh.docx"

    # Чистка временнойго файла
    os.remove(File_Path)
    return response
