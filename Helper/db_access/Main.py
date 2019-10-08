import mimetypes
import os
import sqlite3
import Helper.settings

from django.http import HttpResponse
from xlsxwriter import Workbook

GenderMass = ["женский", "мужской"]

ConcessionMass = ["студент-сирота", "cтудент-инвалид", "cтудент, имеющий детей", "cтудент из многодетной семьи",
                  "cтудент-участник военных действий", "cтудент-чернобылец",
                  "cтудент, имеющий родителей-инвалидов, родителей-пенсионеров", "cтудент из неполной семьи",
                  "cтудент из малоимущей семьи",
                  "cтудент, находящийся на диспансерном учёте с хроническими заболеваниями",
                  "студент, проживающий в общежитии"]

SheetName = ["Сироты", "Инвалиды", "Имеющие детей", "Многодетные семьи",
             "Участник военных действий", "Чернобыльцы",
             "Родители инвалиды, пенсионеры", "Неполная семья",
             "Малоимущая семья",
             "Диспансерный учёт",
             "Общага"]

adr = Helper.settings.BASE_DIR + "/Helper/db_access/db_s.db"
# ТОЛЬКО ДЛЯ REG.RU
#adr.replace('\\','/')



# Функция добавления данных в БД, если такой записи нету
def Insert_Data(gender, group, surname, name, lastname, number, typeconcession, chooseDoc):
    if chooseDoc == '2':
        typeconcession = 10
    typeconcession = ConcessionMass[ int(typeconcession) ]
    gender = GenderMass[int(gender)]
    conn = sqlite3.connect(adr)
    cursor = conn.cursor()
    StringSQLtext = "SELECT * FROM comments WHERE surname = '"+surname+"' AND name = '"+name+"' AND lname = '"+lastname+"' AND group2 = '"+group+"' AND number = '"+number+"' AND typeconcession = '"+typeconcession+"' AND gender = '"+gender+"'"
    cursor.execute(StringSQLtext)
    mysel = cursor.fetchall()
    if mysel != []:
        return
    # добавление записи
    StringSQLtext = "INSERT INTO comments ( surname, name, lname, group2, number, typeconcession, gender, confirm ) VALUES ( '"+surname+"', '"+name+"', '"+lastname+"', '"+group+"', '"+number+"', '"+typeconcession+"', '"+gender+"', '"+'Нет'+"' ); "
    cursor.execute(StringSQLtext)
    conn.commit()
    conn.close()
    return

# Функция генерации экселя по данным из БД
def Get_Data():
    # Подключение БД
    conn = sqlite3.connect(adr)
    c = conn.cursor()

    # Создание книги
    workbook = Workbook('db_accel.xlsx')
    worksheet = []

    # Создание листов по кол-ву элементов (причин)
    for x in range(len(ConcessionMass)):
        worksheet.append(workbook.add_worksheet(SheetName[x]))
        reason = ConcessionMass[x]
        sql = c.execute("SELECT * FROM comments WHERE typeconcession = '" + reason + "'")

        for i, row in enumerate(sql):
            fio = row[1] + ' ' + row[2] + ' ' + row[3]
            for j in range(4, len(row)-1):
                # for j, value in enumerate(row):
                worksheet[x].write(i, 0, fio)
                worksheet[x].write(i, j-3, row[j])

    # mysel = c.execute("SELECT surname, name, lname, group2, number, typeconcession, gender, confirm FROM comments")

    conn.close()
    workbook.close()


    File_Path = os.path.abspath('db_accel.xlsx')
    fp = open(File_Path, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(File_Path)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(File_Path).st_size)
    response['Content-Disposition'] = "attachment; filename=Spisok_Podavshix.xlsx"

    # Чистка временнойго файла
    os.remove(File_Path)
    return response
