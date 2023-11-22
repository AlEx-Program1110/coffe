import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        self.result = self.cur.execute("SELECT * FROM information").fetchall()
        print(self.result)

        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())

