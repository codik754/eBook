from PyQt5 import QtWidgets, QtCore, uic
import mydate
import sqlite3
import time

class Entries(QtWidgets.QLabel):
   """
      Класс для записей 
   """
   clicked = QtCore.pyqtSignal()
   def __init__(self, parent=None):
      QtWidgets.QPushButton.__init__(self, parent)
      self.id = 0 #id записи
      self.title = ""
      self.datetime = mydate.myDate()
      self.bitSel = False #бит выбора 
      self.setText("Пусто")
      self.setStyleSheet("border-bottom:1px solid #000000;background:white;padding:10px;")

   #Возвращение строки для вывода
   def returnHtml(self):
      return "<div style='font-size:13pt;font-weight:bold;'>" + self.title + "</div><br><div>" + self.datetime.getDatetime() +  "</div>"

   #Мышка нажата. Левая кнопка
   def mousePressEvent(self, QMouseEvent):
      #Правый клик
      if QMouseEvent.button() == QtCore.Qt.RightButton:
         print("Правый клик")
      #Первый клик
      if QMouseEvent.button() == QtCore.Qt.LeftButton and self.bitSel == False:
            print("Один клик")
            self.bitSel = True #элемент выбран
            self.changeBackground()
            self.clicked.emit()
      #Второй клик
      elif QMouseEvent.button() == QtCore.Qt.LeftButton and self.bitSel == True:  
            print("Второй клик")
            self.returnBackground()
            self.bitSel = False #сбрасываем бит. Элемент опять становиться не выбраным
            self.clicked.emit()

   #Изменение фона
   def changeBackground(self):pass
      #self.setStyleSheet("font-size:13pt;border-top:1px solid #000000;background:green;")
   
   #Возвращение фона
   def returnBackground(self):pass
      #self.setStyleSheet("font-size:13pt;border-top:1px solid #000000;background:white;")


class PlusWindow(QtWidgets.QWidget):
   """
      Окно для добавления записи
   """
   def __init__(self, parent=None):
      QtWidgets.QWidget.__init__(self, parent)
      uic.loadUi("ui/plus.ui", self)


class MainWindow(QtWidgets.QMainWindow):
   """
      Главное окно приложения
   """
   def __init__(self, parent=None):
      QtWidgets.QMainWindow.__init__(self, parent)
      uic.loadUi("ui/main.ui", self)
      self.setFixedSize(290, 500)
      self.bd = sqlite3.connect('mybd.bd') #подключаемся к БД
      self.cur = self.bd.cursor()

      self.now = mydate.myDate() #атрибут для даты
      self.now.setNow() #устанавливаем текущую дату и время
     
      #Настройки для кнопок
      self.plus.setToolTip("Добавить запись")
      self.plus.setToolTipDuration(3000)
      self.minus.setToolTip("Удалить запись")
      self.minus.setToolTipDuration(3000)

      self.showEntries()
     
   #Показать записи
   def showEntries(self):
      self.vbox = QtWidgets.QVBoxLayout() #Layout для кнопок
      self.vbox.setContentsMargins(0, 0, 0, 0)
      for row in self.cur.execute("SELECT * FROM entries WHERE isdelete = 0 ORDER BY id DESC;"):
         ent = Entries()
         ent.id = row[0]
         ent.title = row[1]
         ent.datetime.setFromString(row[3])
         ent.setText(ent.returnHtml())
         self.vbox.addWidget(ent)
         
      self.vbox.setSpacing(0) #Отступы между элементами
      self.w = QtWidgets.QWidget()
      self.w.setLayout(self.vbox)
      self.scrollArea.setWidget(self.w)
      self.scrollArea.setVerticalScrollBarPolicy(1)
      #self.scrollArea.setStyleSheet("border-radius:10px 10px 10px 10px;")

      self.plus.clicked.connect(self.add)
      self.minus.clicked.connect(self.delete)
      

   #При нажатие на кнопку добавить
   def add(self):
      self.plus = PlusWindow()
      self.plus.show()
      print("Добавить запись")

   #При нажатие на кнопку удалить
   def delete(self):
      print("Удалить запись")

   #При закрытии окна
   def closeEvent(self, e):
      self.bd.close() #Закрывваем соединение с бд
      print("Пока!)")
      

if __name__ == "__main__":
   import sys

   app = QtWidgets.QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec_())
