from PyQt5 import QtWidgets, QtCore, uic
import mydate
import sqlite3

class Entries(QtWidgets.QLabel):
   """
      Класс для записей 
   """
   clicked = QtCore.pyqtSignal()
   openentry = QtCore.pyqtSignal(int)
   def __init__(self, parent=None):
      QtWidgets.QPushButton.__init__(self, parent)
      self.n = 0 # порядковый номер в элементе
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
         self.openentry.emit(self.n)
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
   send_data = QtCore.pyqtSignal(str, str)
   def __init__(self, parent=None):
      QtWidgets.QWidget.__init__(self, parent)
      uic.loadUi("ui/plus.ui", self)
      #Указываем тип окна
      self.setWindowFlags(QtCore.Qt.Dialog)
      #Фиксированный размер окна
      self.setFixedSize(500, 400)
      #Делаем окно модальным
      self.setWindowModality(QtCore.Qt.ApplicationModal)
      #Настройка кнопок
      self.bAdd.clicked.connect(self.add)
      self.bReset.clicked.connect(self.reset)
      #Окно предупреждения
      self.message = QtWidgets.QMessageBox(self)
   
   #Сброс значений в полях
   def reset(self):
      self.tName.clear()
      self.tText.clear()
      
   def add(self):
      if self.tName.text() == "" and self.tText.toPlainText() == "":
         self.message.information(window, "Сообщение", "Поля пусты. Введите значения", buttons=QtWidgets.QMessageBox.Close)
      elif self.tName.text() == "":
         self.message.information(window, "Сообщение", "Поля название пустое. Введите значение", buttons=QtWidgets.QMessageBox.Close)
      elif self.tText.toPlainText() == "":
         self.message.information(window, "Сообщение", "Поля текст пустое. Введите значение", buttons=QtWidgets.QMessageBox.Close)
      else:
         self.send_data.emit(self.tName.text(), self.tText.toPlainText())
         self.close()

class ShowWindow(QtWidgets.QWidget):
   """
      Окно для отображения записи
   """
   def __init__(self, parent=None, name="Без названия", text=""):
      QtWidgets.QWidget.__init__(self, parent)
      uic.loadUi("ui/show.ui", self)
      self.setWindowFlags(QtCore.Qt.Dialog)
      self.setFixedSize(500, 400)
      self.setWindowModality(QtCore.Qt.ApplicationModal)
      self.lName.setText(name)
      self.tText.setText(text)


class MainWindow(QtWidgets.QMainWindow):
   """
      Главное окно приложения
   """
   def __init__(self, parent=None):
      QtWidgets.QMainWindow.__init__(self, parent)
      uic.loadUi("ui/main.ui", self)
      self.setFixedSize(290, 500)

      self.plusWindow = PlusWindow() #окно добавления записи
      self.plusWindow.send_data[str, str].connect(self.addToBD)

      self.bd = sqlite3.connect('mybd.bd') #подключаемся к БД
      self.cur = self.bd.cursor()

      self.now = mydate.myDate() #атрибут для даты
     
      #Настройки для кнопок
      self.plus.setToolTip("Добавить запись")
      self.plus.setToolTipDuration(3000)
      self.minus.setToolTip("Удалить запись")
      self.minus.setToolTipDuration(3000)
      self.plus.clicked.connect(self.add)
      self.minus.clicked.connect(self.delete)
      
      self.showEntries()
   
   #Показать записи в меню
   def showEntries(self):
      self.vbox = QtWidgets.QVBoxLayout() #Layout для кнопок
      self.vbox.setContentsMargins(0, 0, 0, 0)
      i = 0 # счетчик
      for row in self.cur.execute("SELECT * FROM entries WHERE isdelete = 0 ORDER BY id DESC;"):
         ent = Entries()
         ent.n = i
         i += 1
         ent.id = row[0]
         ent.title = row[1]
         ent.datetime.setFromString(row[3])
         ent.setText(ent.returnHtml())
         ent.openentry[int].connect(self.showEntry)
         self.vbox.addWidget(ent)
         
      self.vbox.setSpacing(0) #Отступы между элементами
      self.w = QtWidgets.QWidget()
      self.w.setLayout(self.vbox)
      self.scrollArea.setWidget(self.w)
      self.scrollArea.setVerticalScrollBarPolicy(1)
      #self.scrollArea.setStyleSheet("border-radius:10px 10px 10px 10px;")

   #Отображение записи
   def showEntry(self, n):
      print("Показываю запись:", n)
      ent = self.vbox.itemAt(n).widget()
      query = "SELECT * FROM entries WHERE id = " + str(ent.id) + ";"
      t = self.cur.execute(query).fetchone()
      self.entry = ShowWindow(name=ent.title, text=t[2])
      self.entry.show()

   #При нажатие на кнопку добавить
   def add(self):
      self.plusWindow.show()
   
   #Добавление в БД
   def addToBD(self, name, text):
     self.now.setNow() #устанавливаем текущую дату и время
     query = "INSERT INTO entries (name, text, date, isdelete) VALUES ('" + name + "', '" + text + "', '" + self.now.getDatetime() + "', 0);"
     self.cur.execute(query)
     self.bd.commit()
     self.showEntries()

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
