import re
import threading
import os
import datetime
import Helper.settings
import sys, shutil

from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


from Helper import settings
from Helper.generadeword.Main import CreateWord
from Helper.db_access.Main import Insert_Data, Get_Data as Data_Base
from Helper.rsa_path.Main import Get_Path

from django.conf import settings
from shutil import copyfile


#from g_recaptcha.validate_recaptcha import validate_captcha

# путь для получения данных, выдается в шифрованном виде
Patch_Of_Get = "Non"

NO_REDIR = { "/gen" }

#@validate_captcha
def Set_Data(request):
    if request.method == "GET":
        name = request.GET.get('name', '')
        lname = request.GET.get('lname', '')
        surname = request.GET.get('surname', '')
        group = request.GET.get('group', '')
        number = request.GET.get('number', '')
        typeconcession = request.GET.get('typeconcession', '')
        gender = request.GET.get('gender', '')
        chooseDoc = request.GET.get('chooseDoc', '')

        # урезание строки
        gender = re.sub(" +", ' ', gender.strip())
        group = re.sub(" +", ' ', group.strip())
        surname = re.sub(" +", ' ', surname.strip())
        name = re.sub(" +", ' ', name.strip())
        lname = re.sub(" +", ' ', lname.strip())
        number = re.sub(" +", ' ', number.strip())
        typeconcession = re.sub(" +", ' ', typeconcession.strip())
        chooseDoc = re.sub(" +", ' ', chooseDoc.strip())

        # UpperCase на группу
        group = group.upper()

        respons = CreateWord(gender, group, surname, name, lname, number, typeconcession, chooseDoc)
        if respons != "Error Gender" and respons != "Error NoData" and respons != "Error Len":
            t = threading.Thread(target=Insert_Data, args=(gender, group, surname, name, lname, number, typeconcession, chooseDoc))
            t.daemon = True
            t.start()
            return respons
    return HttpResponse(respons)

def copytree(src, dst, symlinks=0):
  print ("copy tree " + src)
  names = os.listdir(src)
  if not os.path.exists(dst):
    os.mkdir(dst)
  for name in names:
    srcname = os.path.join(src, name)
    dstname = os.path.join(dst, name)
    try:
      if symlinks and os.path.islink(srcname):
        linkto = os.readlink(srcname)
        os.symlink(linkto, dstname)
      elif os.path.isdir(srcname):
        copytree(srcname, dstname, symlinks)
      else:
        shutil.copy2(srcname, dstname)
    except (IOError, os.error):
      print ("Can't copy %s to %s: %s", srcname, dstname, str(why))

# Рендер главной страницы
#@validate_captcha
def Index(request):
    return render(request, 'index.html')

def Webstat(request):
    copytree('/var/www/u0825496/data/www/ruthelp.ru/webstat/', '/var/www/u0825496/data/www/ruthelp.ru/Helper/templates/webstat')
    return render(request, 'webstat/index.html')

# Перенапрвление на главную страницу
def Any_Page(request):
    return redirect("/index")

# Запрос на создание ссылки для загрузки
def Get_Data(request):
    (Patch,Patch_Cript) = Get_Path()
    global Patch_Of_Get
    Patch_Of_Get = Patch
    print("Генерация динамической ссылки для загрузки")
    threading.Timer(10, Clear_Page).start()
    return HttpResponse(Patch_Cript)

# Удаление ссылки на загрузку
def Clear_Page():
    print("Очистка динамической ссылки для загрузки")
    global Patch_Of_Get
    Patch_Of_Get = "Non"
    return

# Выдача данных из базы данных
def Page_Return_Data(request, path):
    global Patch_Of_Get
    if path == Patch_Of_Get and Patch_Of_Get != "Non":
        Patch_Of_Get = "Non"
        return Data_Base()
    return redirect("/index")

# Бэкап
def Backup(request):
    adr = Helper.settings.BASE_DIR + "/Helper/db_access/db_s.db"
    time = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    adrout = Helper.settings.BASE_DIR + "/Helper/db_access/backup/db_s-"+ time + ".db"
    adr.replace('\\','/')
    adrout.replace('\\','/')

    copyfile(adr, adrout)
    return redirect("/index")
