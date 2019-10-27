import os
import random
import sys
import threading
import urllib.request

import rsa
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Client import design
from Client.key import Private_Key


def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """

    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


@thread
def processing(signal):
    """
    Эмулирует обработку (скачивание) каких-то данных
    """
    res = ["THREAD STARTED"]
    signal.emit(res)  # Посылаем сигнал в котором передаём полученные данные


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    save_signal = QtCore.pyqtSignal(list, name='save_signal')

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.labelName.setText("Блокиратор кнопок")
        self.groupBu.setFixedWidth(132)
        # При нажатии на кнопку запускаем обработку данных
        self.buSave.clicked.connect(lambda: processing(self.save_signal))
        self.save_signal.connect(self.signal_save_handler, QtCore.Qt.QueuedConnection)

        self.horizontalSlider.valueChanged.connect(self.change_slider)

    def signal_save_handler(self, data):  # Вызывается для обработки сигнала
        print(data)
        self.labelSave.setText(self.save_xlsx())

    def change_slider(self):
        # Блок (слева)
        if self.horizontalSlider.value() < 15:
            self.labelUnlock.setStyleSheet("color : black")
            self.labelLock.setStyleSheet("color: #8d8d8d")
            self.groupBu.setEnabled(1)
        # Блок (справа)
        elif self.horizontalSlider.value() > 85:
            self.labelUnlock.setStyleSheet("color : #8d8d8d")
            self.labelLock.setStyleSheet("color: black")
            self.groupBu.setEnabled(0)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        size = self.size()

        def draw():
            for i in range(1000):
                x = random.randint(1, size.width() - 1)
                y = random.randint(1, size.height() - 1)
                qp.drawPoint(x, y)

        qp.setPen(Qt.red)
        draw()
        qp.setPen(Qt.blue)
        draw()
        qp.setPen(Qt.green)
        draw()
        qp.setPen(Qt.yellow)
        draw()
        qp.setPen(Qt.magenta)
        draw()

    def save_xlsx(self):
        self.labelSave.setText("Получение пути")
        crypto = ""
        try:
            fp = urllib.request.urlopen("https://ruthelp.ru/getdata/")
            mybytes = fp.read()
            fp.close()
        except BaseException:
            # self.labelSave.setText("Сервер недоступен")
            return "Произошла ошибка при загрузке данных с сервера, проверьте его работу!"

        self.labelSave.setText("Расшифровка пути")
        try:
            crypto = rsa.decrypt(mybytes, Private_Key)
        except BaseException:
            self.labelSave.setText("Ошибка расшифровки")
            return "Произошла ошибка при попытке расшифровки, проверьте правильность ключа!"

        self.labelSave.setText("Загрузка файла")
        try:
            url = "https://ruthelp.ru/pages/" + crypto.decode("utf-8")
            urllib.request.urlretrieve(url, 'Spisok_podavshih.xlsx')
        except BaseException:
            self.labelSave.setText("Ошибка загрузки")
            return "Произошла ошибка при скачивании файла!"
        self.labelSave.setText("Загрузка успешна")
        return "Загрузка успешна"

    def browse_folder(self):
        self.listWidget.clear()  # На случай, если в списке уже есть элементы
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            for file_name in os.listdir(directory):  # для каждого файла в директории
                self.listWidget.addItem(file_name)  # добавить файл в listWidget


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()
