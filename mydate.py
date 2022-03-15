#Модуль, описывающий класс для времени

import datetime

class myDate():
   """ 
      Класс для времени и даты
   """
   def __init__(self):
      self.day = 0 
      self.month = 0 
      self.year = 0 
      self.hour = 0 
      self.minute = 0 
      self.second = 0 

   #Установка текущей даты и времени
   def setNow(self):
      temp = datetime.datetime.today()
      self.day = temp.day
      self.month = temp.month
      self.year = temp.year
      self.hour = temp.hour
      self.minute = temp.minute
      self.second = temp.second
   
   #Установка значения из строки
   def setFromString(self, string):
      s = string.split() #разделяем основную строку даты
      s1 = s[0].split('.') #это день, месяц, год
      self.day = int(s1[0])
      self.month = int(s1[1])
      self.year = int(s1[2])
      s2 = s[1].split(':')# это час, минуты и секунды
      self.hour = int(s2[0])
      self.minute = int(s2[1])
      self.second = int(s2[2])

   #Метод для получения красивого числа в формате XX
   def getPretyNumber(iself, n = 0): 
      if n - 10 < 0:
         return "0" + str(n)
      else:
         return str(n)

   #Метод, который возращает дату в формате XX.XX.XXXX
   def getDate(self):
      return self.getPretyNumber(self.day) + "." + self.getPretyNumber(self.month) + "." + str(self.year)

   #Метод, который возвращает время в формате XX:XX:XX
   def getTime(self):
      return self.getPretyNumber(self.hour) + ":" + self.getPretyNumber(self.minute) + ":" + self.getPretyNumber(self.second)

   #Метод, который возвращает дату и время
   def getDatetime(self):
      return self.getPretyNumber(self.day) + "." + self.getPretyNumber(self.month) + "." + str(self.year) + " " + self.getPretyNumber(self.hour) + ":" + self.getPretyNumber(self.minute) + ":" + self.getPretyNumber(self.second)
   def __str__(self):
      return "Класс для времени" 

