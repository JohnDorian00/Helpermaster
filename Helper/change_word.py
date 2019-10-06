# проверка на гласную
def checkVowels(letter):
  vowels = "аеёюяиоуыэ"

  if vowels.find(letter) != -1:
    #print(letter, " - гласная")
    return True
  else:
    #print(letter, " - согласная")
    return False


# Фамилии
def Genitive_SecondName(F, O):
  Flag = 1
  # если фамилия двойная
  if F.find("-")!=-1:
      Flag = 0
      A = F.split("-")
      A[0] = A[0].strip()
      A[0] = A[0].capitalize()
      A[1] = A[1].strip()
      A[1] = A[1].capitalize()
  F = F.strip()
  F = F.capitalize()
  # фамилии на -ская, -цкая
  if F[-4:] == 'ская' or F[-4:] == 'цкая':
      F = F[0:-2]
      F = F + "ой"
  # Женские фамилии на -ова, -ева, -ина
  if F[-3:] == 'ова' or F[-3:] == 'ева' or F[-3:] == 'ина' or F[-3:] == 'ёва':
      F = F[0:-1]
      F = F + "ой"
  # женские фамилии, которые оканчиваются на согласную, не склоняются!
  if checkVowels(F[-1:]) != True and O[-3:] == 'вна':
      F = F
  # мужские фамилии, которые оканчиваются на согласную склоняются
  if checkVowels(F[-1:]) != True and O[-3:] == 'вич':
      if (F[-1] == 'ь' ):
          F = F[:-1] + "я"
      else:
          F = F + "а"
  # Фамилии, которые оканчиваются на гласные -е, -и, -о, -у, -ы, -э, -ю не склоняются.
  if (F[-1:] == 'е' or F[-1:] == 'и' or F[-1:] == 'о' or F[-1:] == 'у' or F[-1:] == 'ы' or F[-1:] == 'э'
          or F[-1:] == 'ю' or F[-1:] == 'их' or F[-1:] == 'ых'):
      F = F
  # в конце фамилии имеется сразу две гласные (то есть букве -а предшествует другая гласная), то она не склоняется.
  if F[-1] == 'а' and F[-2] == True:
      F = F
  #  Женские фамилии, оканчивающиеся на -ая
  if F[-2:] == 'ая' and O[-3:] == 'вна':
      F = F + "ой"
  # Фамилии, оканчивающиеся на -ов/ев, -ин/ын
  if F[-2:] == 'ов' or F[-2:] == 'ев' or F[-2:] == 'ин' or F[-2:] == 'ёв' or F[-2:] == 'ын':
      F = F + "а"
  # фамилии на -ский, -цкий,-ый,-ой,-ий
  if (F[-4:] == 'ский' or F[-4:] == 'цкий' or F[-2:] == 'ый' or F[-2:] == 'ий' or F[-2:] == 'ой') and O[-3:] == 'вич':
      F = F[0:-2]
      F = F + "ого"
  return F
  # для двойной фамилии
  if (Flag == 1):
      F = Fam(F)
  else:
      F = Fam(A[0]) + '-' + Fam(A[1])
# Имена
def Genitive_Name(I, O):
  I = I.strip()
  I = I.capitalize()
  # Мужские и женские имена, оканчивающиеся на –а:
  if I[-1] == "а":
      if I.lower() == "ольга":
          I = I[0:-1]
          I = I + 'и'
      else:
          I = I[0:-1]
          I = I + 'ы'

  # Мужские и женские имена, оканчивающиеся на -я, -ья, -ия, -ея:
  if I[-1:] == 'я' or I[-2:] == 'ья' or I[-2:] == 'ия' or I[-2:] == 'ея':
      I = I[0:-1]
      I = I + "и"
  # Мужские имена, оканчивающиеся на –й
  if I[-1] == "й" and O[-3:] == 'вич':
      I = I[0:-1]
      I = I + 'я'
  #  Женские имена оканчивающиеся на -ь
  if I[-1] == "ь" and O[-3:] == 'вна':
      I = I[0:-1]
      I = I + 'и'
  #  Мужские имена оканчивающиеся на -ь
  if I[-1] == "ь" and O[-3:] == 'вич':
      I = I[0:-1]
      I = I + 'я'
  # Мужские имена, оканчивающиеся на согласный
  if ( checkVowels(I[-1:]) == False and ( O[-3:] == 'вич' or O.find("оглы") or O.find("угли") or O.find("огли") or O.find("оглу") )):
    #print("Мужское имя на согласную")
    I = I + 'а'

  #print("O = ", O[-3:], "")


  # Имена с беглой гласной
  if I == "Павел":
      I = "Павла"
  elif I == "Лев":
      I = "Льва"

  return I
# Отчества
def Genitive_MiddleName(O):
  # удаляет пробелы между отчеством и кызы/оглы и тд.
  if O.find("оглы") or O.find("кызы") or O.find("угли") or O.find("огли") or O.find("оглу"):
      O = ' '.join(map(str.strip, O.split()))
  O = O.strip()
  O = O.capitalize()
  if O[-3:] == "вна":
      O = O[0:-1]
      O = O + 'ы'
  if O[-3:] == "вич":
      O = O + 'а'
  return O

def takeWord(F,I,O):
    FIO = {Genitive_SecondName(F),Genitive_Name(I),Genitive_MiddleName(O)}
    F = Genitive_SecondName(F)
    I = Genitive_Name(I)
    O = Genitive_MiddleName(O)
    print(F, I, O)
    return FIO
