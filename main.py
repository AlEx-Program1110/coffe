import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QPushButton, QLabel


# "ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"

class Coffe_menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.information_coffe: QTableWidget
        self.information_coffe.setColumnCount(7)
        self.information_coffe.setHorizontalHeaderLabels(
            ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        self.result = self.cur.execute("SELECT * FROM information").fetchall()

        self.con.close()
        self.information_coffe.setRowCount(len(self.result))
        for i in range(len(self.result)):
            for j in range(len(self.result[i])):
                self.information_coffe.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))

        self.add: QPushButton
        self.change: QPushButton

        self.add.clicked.connect(self.push_add)
        self.change.clicked.connect(self.push_change)

    def push_add(self):
        print('add')
        self.ex = Dialog_add_change(self, 0)
        self.ex.show()

    def push_change(self):
        print('change')
        self.ex = Dialog_add_change(self, 1)
        self.ex.show()


class Dialog_add_change(QMainWindow):
    def __init__(self, parent, move):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.data_new: QLineEdit
        self.label: QLabel

        if move:
            self.label.setText('Измените')
        else:
            self.label.setText('Добавьте новое кофе')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffe_menu()
    ex.show()
    sys.exit(app.exec())
