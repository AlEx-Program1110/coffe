import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow, QTableWidget


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffe_menu()
    ex.show()
    sys.exit(app.exec())
