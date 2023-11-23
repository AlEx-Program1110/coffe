import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QPushButton, QLabel


# при нажатии на ячейку в таблице у вас будет спрашивать на что хотите изменить
# при нажатии добавить вводите новое имя кофе
# после любых добавлений или изменений не забутите обновить
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
        self.update: QPushButton

        self.add.clicked.connect(self.push_add)
        self.update.clicked.connect(self.push_update)
        self.information_coffe.cellClicked.connect(self.item_changed)
        self.vrem = 0

    def push_add(self):
        self.ex = Dialog_add_change(self, 0)
        self.ex.show()

    def push_update(self):
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

    def item_changed(self, row, col):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.ex = Dialog_add_change(self, 1, row, col)
        self.ex.show()


class Dialog_add_change(QMainWindow):
    def __init__(self, parent, move, row=0, col=0):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.row = row
        self.col = col
        self.data_new: QLineEdit
        self.label: QLabel
        self.save_button: QPushButton

        self.save_button.clicked.connect(self.push_save)
        self.move = move
        if move:
            self.label.setText('Измените')
        else:
            self.label.setText('Добавьте новое кофе(введите название кофе и сохраните)')

    def push_save(self):
        if self.move:
            data_SQL = ['ID', 'title', 'degree_fire', 'structure', 'data', 'price', 'size']
            name = self.data_new.text()
            self.con = sqlite3.connect("coffee.sqlite")
            self.cur = self.con.cursor()

            self.cur.execute(f"""UPDATE information
                                    SET {data_SQL[self.col]} = '{name}'
                                    WHERE ID = {self.row + 1}""")

            self.con.commit()

            self.con.close()
        else:
            name = self.data_new.text()
            # INSERT INTO genres VALUES (45, 'Научные'), (46, 'Сказки')
            self.con = sqlite3.connect("coffee.sqlite")
            self.cur = self.con.cursor()

            self.cur.execute(f"INSERT INTO information(title) VALUES ('{name}')")

            self.con.commit()

            self.con.close()

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffe_menu()
    ex.show()
    sys.exit(app.exec())
