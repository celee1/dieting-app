from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QFrame, QLineEdit, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore
from sqlite3 import IntegrityError, OperationalError
import sqlite3
from datetime import datetime
import sys


class DietingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = sqlite3.connect(r'App_projects\dieting_app\food_database.db')
        self.cursor = self.db.cursor()
        self.formatted = datetime.now().strftime("%Y-%m-%d")

        self.setGeometry(0, 0, 900, 900)
        self.setWindowTitle('Dieting app')
        self.setStyleSheet('background: #ffffff')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.show()

        self.grid = QGridLayout(self.central_widget)

        self.label = QLabel(self.central_widget)
        self.label.setText('Dieting app')
        self.label.setStyleSheet('color: 000000;' + "font-size: 50px")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.label, 0, 1)

        self.food_button = QPushButton('new entry')
        self.food_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                       "border-radius: 45px;" +
                                       "font-size: 35px;" +
                                       "color: '#000000';" +
                                       "background: '#08fff0';" +
                                       "padding: 25px;}" +
                                       "*:hover{background: '#f8ff08';}"
                                       )
        self.food_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.food_button.clicked.connect(self.new_entry)
        self.grid.addWidget(self.food_button, 1, 0)

        self.macros_button = QPushButton('macros window')
        self.macros_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                         "border-radius: 45px;" +
                                         "font-size: 35px;" +
                                         "color: '#000000';" +
                                         "background: '#08fff0';" +
                                         "padding: 25px;}" +
                                         "*:hover{background: '#f8ff08';}"
                                         )
        self.macros_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.macros_button.clicked.connect(self.macros_window)
        self.grid.addWidget(self.macros_button, 1, 1)

        self.new_food_button = QPushButton('new food type')
        self.new_food_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                           "border-radius: 45px;" +
                                           "font-size: 35px;" +
                                           "color: '#000000';" +
                                           "background: '#08fff0';" +
                                           "padding: 25px;}" +
                                           "*:hover{background: '#f8ff08';}"
                                           )
        self.new_food_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.new_food_button.clicked.connect(self.new_food_type)
        self.grid.addWidget(self.new_food_button, 1, 2)

        self.look_up_button = QPushButton('search database')
        self.look_up_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                          "border-radius: 45px;" +
                                          "font-size: 35px;" +
                                          "color: '#000000';" +
                                          "background: '#08fff0';" +
                                          "padding: 25px;}" +
                                          "*:hover{background: '#f8ff08';}"
                                          )
        self.look_up_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.look_up_button.clicked.connect(self.look_up_window)
        self.grid.addWidget(self.look_up_button, 2, 0)

        self.close_app_button = QPushButton('close app')
        self.close_app_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                            "border-radius: 45px;" +
                                            "font-size: 35px;" +
                                            "color: '#000000';" +
                                            "background: '#08fff0';" +
                                            "padding: 25px;}" +
                                            "*:hover{background: '#f8ff08';}"
                                            )
        self.close_app_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.close_app_button.clicked.connect(self.close_app)
        self.grid.addWidget(self.close_app_button, 2, 2)

    def new_entry(self):
        self.new_window = NewEntry()
        self.new_window.show()

    def macros_window(self):
        self.new_window = Macros()
        self.new_window.show()

    def new_food_type(self):
        self.new_window = NewFood()
        self.new_window.show()

    def look_up_window(self):
        self.new_window = LookUpWindow()
        self.new_window.show()

    def close_app(self):
        try:
            self.new_window.close()
        except AttributeError:
            pass
        self.close()


class NewEntry(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 600, 400)
        self.setWindowTitle('Food entry')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.frame_1 = QFrame(self)
        self.grid.addWidget(self.frame_1, 1, 0)
        self.grid_1 = QGridLayout(self.frame_1)

        self.food_name_label = QLabel(self.frame_1)
        self.food_name_label.setText('food name')
        self.food_name_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.food_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.food_name_label, 0, 0)

        self.food_name_edit = QLineEdit(self.frame_1)
        self.food_name_edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                          "border-radius: 45px;" +
                                          "font-size: 25px;" +
                                          "padding: 0 25px;" +
                                          "color: '#000000';}")
        self.food_name_edit.setFocus()
        self.grid_1.addWidget(self.food_name_edit, 1, 0)

        self.food_quantity_label = QLabel(self.frame_1)
        self.food_quantity_label.setText('food quantity (g)')
        self.food_quantity_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.food_quantity_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.food_quantity_label, 2, 0)

        self.food_quantity_edit = QLineEdit(self.frame_1)
        self.food_quantity_edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                              "border-radius: 45px;" +
                                              "font-size: 25px;" +
                                              "padding: 0 25px;" +
                                              "color: '#000000';}")
        self.grid_1.addWidget(self.food_quantity_edit, 3, 0)

        self.add_button = QPushButton('add a food')
        self.add_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                      "border-radius: 20px;" +
                                      "font-size: 20px;" +
                                      "color: '#000000';" +
                                      "background: '#08fff0';" +
                                      "padding: 25px;}" +
                                      "*:hover{background: '#f8ff08';}"
                                      )
        self.add_button.clicked.connect(self.add_food)
        self.add_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.grid_1.addWidget(self.add_button, 0, 1)

        self.remove_button = QPushButton('remove a food')
        self.remove_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                         "border-radius: 20px;" +
                                         "font-size: 20px;" +
                                         "color: '#000000';" +
                                         "background: '#08fff0';" +
                                         "padding: 25px;}" +
                                         "*:hover{background: '#f8ff08';}"
                                         )
        self.remove_button.clicked.connect(self.remove_food)
        self.remove_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))

        self.grid_1.addWidget(self.remove_button, 1, 1)

        self.clear_button = QPushButton('clear plan')
        self.clear_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                        "border-radius: 20px;" +
                                        "font-size: 20px;" +
                                        "color: '#000000';" +
                                        "background: '#08fff0';" +
                                        "padding: 25px;}" +
                                        "*:hover{background: '#f8ff08';}"
                                        )
        self.clear_button.clicked.connect(self.clear_plan)
        self.clear_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.grid_1.addWidget(self.clear_button, 2, 1)

        self.select_button = QPushButton('select a food')
        self.select_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                         "border-radius: 20px;" +
                                         "font-size: 20px;" +
                                         "color: '#000000';" +
                                         "background: '#08fff0';" +
                                         "padding: 25px;}" +
                                         "*:hover{background: '#f8ff08';}"
                                         )
        self.select_button.clicked.connect(self.select_food)
        self.select_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.grid_1.addWidget(self.select_button, 3, 1)

        self.close_button = QPushButton('close window')
        self.close_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                        "border-radius: 20px;" +
                                        "font-size: 20px;" +
                                        "color: '#000000';" +
                                        "background: '#08fff0';" +
                                        "padding: 25px;}" +
                                        "*:hover{background: '#f8ff08';}"
                                        )
        self.close_button.clicked.connect(self.close)
        self.close_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.grid_1.addWidget(self.close_button, 4, 1)

        self.frame_2 = QFrame(self)
        self.grid.addWidget(self.frame_2, 0, 0)
        self.grid_2 = QGridLayout(self.frame_2)

        self.total_label = QLabel(self.frame_2)
        self.total_label.setText('total calories')
        self.total_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.total_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_2.addWidget(self.total_label, 1, 0)

        self.protein_label = QLabel(self.frame_2)
        self.protein_label.setText('total protein')
        self.protein_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.protein_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_2.addWidget(self.protein_label, 2, 0)

        self.fat_label = QLabel(self.frame_2)
        self.fat_label.setText('total fat')
        self.fat_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.fat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_2.addWidget(self.fat_label, 3, 0)

        self.carbohydrates_label = QLabel(self.frame_2)
        self.carbohydrates_label.setText('total carbohydrates')
        self.carbohydrates_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.carbohydrates_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_2.addWidget(self.carbohydrates_label, 4, 0)

        self.gs = 'g'
        self.num_total_label = QLabel(self.frame_2)
        self.num_total_label.setText('0 kcal')
        self.num_total_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.num_total_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_2.addWidget(self.num_total_label, 1, 1)

        self.num_protein_label = QLabel(self.frame_2)
        self.num_protein_label.setText(f'0 {self.gs}')
        self.num_protein_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.num_protein_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_2.addWidget(self.num_protein_label, 2, 1)

        self.num_fat_label = QLabel(self.frame_2)
        self.num_fat_label.setText(f'0 {self.gs}')
        self.num_fat_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.num_fat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_2.addWidget(self.num_fat_label, 3, 1)

        self.num_carbohydrates_label = QLabel(self.frame_2)
        self.num_carbohydrates_label.setText(f'0 {self.gs}')
        self.num_carbohydrates_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.num_carbohydrates_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_2.addWidget(self.num_carbohydrates_label, 4, 1)

        try:
            self.insert_data()
        except OperationalError:
            pass

        [item.setMaximumWidth(200) for item in self.frame_1.children() if type(
            item) != QGridLayout]

    def insert_data(self):
        daily_intake = d.cursor.execute(
            f'SELECT * FROM "{d.formatted}"').fetchall()

        self.num_total_label.setText(
            str(round(sum([item[1] for item in daily_intake]), 2)))

        self.num_protein_label.setText(
            str(round(sum([item[2] for item in daily_intake]), 2)))

        self.num_fat_label.setText(
            str(round(sum([item[3] for item in daily_intake]), 2)))

        self.num_carbohydrates_label.setText(
            str(round(sum([item[4] for item in daily_intake]), 2)))

    def add_food(self):
        try:
            food_to_add = self.food_name_edit.text().lower()
            quantity_to_add = float(self.food_quantity_edit.text())
        except ValueError:
            msg = QMessageBox(QMessageBox.Warning, 'Missing food details',
                              'Please enter the required details, food name and quantity')
            msg.exec_()
            return

        try:
            result = d.cursor.execute(
                f"SELECT * FROM Foods WHERE food_name = '{food_to_add}'").fetchall()[0]
        except IndexError:
            msg = QMessageBox(QMessageBox.Warning, 'Food not found',
                              'Food not found in the database')
            msg.exec_()
            return

        new_num_calories = round(result[1] / 100 * quantity_to_add, 2)
        new_num_of_protein = round(result[2] / 100 * quantity_to_add, 2)
        new_num_of_fat = round(result[3] / 100 * quantity_to_add, 2)
        new_num_of_carbohydrates = round(result[4] / 100 * quantity_to_add, 2)

        table = d.cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{d.formatted}';").fetchall()
        if table == []:
            d.cursor.execute(
                f"CREATE TABLE '{d.formatted}' (food_name TEXT, calories REAL, protein REAL, lipids REAL, carbohydrates REAL, id INTEGER)")
            d.db.commit()

        n_of_rows = int(d.cursor.execute(
            f'SELECT COUNT(*) from "{d.formatted}"').fetchall()[0][0]) + 1

        d.cursor.execute(
            f"INSERT INTO '{d.formatted}' VALUES ('{food_to_add}', '{new_num_calories}', '{new_num_of_protein}', '{new_num_of_fat}', '{new_num_of_carbohydrates}', '{n_of_rows}')")
        d.db.commit()

        self.insert_data()
        self.food_name_edit.setText('')
        self.food_quantity_edit.setText('')

        self.food_name_edit.setFocus()

    def remove_food(self):

        d.cursor.execute(f'SELECT COUNT(*) from "{d.formatted}"')
        n_of_rows = d.cursor.fetchall()[0][0]

        d.cursor.execute(
            f'DELETE FROM "{d.formatted}" WHERE id={n_of_rows};')
        d.db.commit()

        self.insert_data()
        self.food_name_edit.setFocus()

    def clear_plan(self):
        try:
            d.cursor.execute(f'SELECT COUNT(*) from "{d.formatted}"')

            d.cursor.execute(f'DELETE FROM "{d.formatted}";')
            d.db.commit()

            self.insert_data()

        except OperationalError:
            msg = QMessageBox(QMessageBox.Warning, 'Table does not exist',
                              'No table with this name exists in the database')
            msg.exec_()

    def select_food(self):
        self.select = SelectFood()
        self.select.show()


class SelectFood(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 600, 400)
        self.setWindowTitle('Select a food')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.buttons = []

        self.get_foods()

        self.label = QLabel(self)
        self.label.setText('Search for food: ')
        self.label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.grid.addWidget(self.label, self.row + 1, 0)

        self.edit = TextEdit(self)
        self.edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                "border-radius: 45px;" +
                                "font-size: 25px;" +
                                "padding: 0 25px;" +
                                "color: '#000000';}")
        self.edit.setFocus()
        self.edit.textEdited.connect(self.filter_foods)
        self.grid.addWidget(self.edit, self.row + 1, 1)

    def get_foods(self):
        foods = [item[0] for item in d.cursor.execute(
            'SELECT food_name FROM foods').fetchall()]
        self.row = 0
        column = 0
        for food in foods:
            button = QPushButton(f'{food}')
            button.setStyleSheet("*{border: 2px solid '#000000';" +
                                 "border-radius: 20px;" +
                                 "font-size: 20px;" +
                                 "color: '#000000';" +
                                 "background: '#08fff0';" +
                                 "padding: 25px;}" +
                                 "*:hover{background: '#f8ff08';}"
                                 )
            self.buttons.append(button)
            button.clicked.connect(self.add_text)
            self.grid.addWidget(button, self.row, column)
            column += 1
            if column != 0:
                if column % 5 == 0:
                    self.row += 1
                    column = 0

    def add_text(self):
        text = self.sender().text()
        d.new_window.food_name_edit.setText(text)
        d.new_window.food_quantity_edit.setFocus()
        self.close()

    def filter_foods(self):
        [button.close()
         for button in self.buttons if self.edit.text() not in button.text()]

    def show_buttons(self):
        [button.show() for button in self.buttons]


class TextEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            try:
                d.new_window.select.edit.setText(
                    d.new_window.select.edit.text()[:-1])
                d.new_window.select.show_buttons()
                d.new_window.select.filter_foods()
            except IndexError:
                pass
        super(TextEdit, self).keyPressEvent(event)


class Macros(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle('Macros window')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.frame_1 = QFrame(self)
        self.grid.addWidget(self.frame_1)

        self.grid_1 = QGridLayout(self.frame_1)

        self.main_label = QLabel(self.frame_1)
        self.main_label.setText('macros distribution')
        self.main_label.setStyleSheet(
            'color: 000000;' + "font-size: 40px")
        self.main_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.main_label, 0, 0, 1, 2)

        self.total_label = QLabel(self.frame_1)
        self.total_label.setText('perc total')
        self.total_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.total_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.total_label, 1, 0)

        self.protein_label = QLabel(self.frame_1)
        self.protein_label.setText('perc protein')
        self.protein_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.protein_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.protein_label, 2, 0)

        self.fat_label = QLabel(self.frame_1)
        self.fat_label.setText('perc fat')
        self.fat_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.fat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.fat_label, 3, 0)

        self.carbohydrates_label = QLabel(self.frame_1)
        self.carbohydrates_label.setText('perc carbohydrates')
        self.carbohydrates_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.carbohydrates_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.carbohydrates_label, 4, 0)

        self.perc_total_label = QLabel(self.frame_1)
        self.perc_total_label.setText('0 %')
        self.perc_total_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.perc_total_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.perc_total_label, 1, 1)

        self.perc_protein_label = QLabel(self.frame_1)
        self.perc_protein_label.setText('0 %')
        self.perc_protein_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.perc_protein_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.perc_protein_label, 2, 1)

        self.perc_fat_label = QLabel(self.frame_1)
        self.perc_fat_label.setText('0 %')
        self.perc_fat_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.perc_fat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.perc_fat_label, 3, 1)

        self.perc_carbohydrates_label = QLabel(self.frame_1)
        self.perc_carbohydrates_label.setText('0 %')
        self.perc_carbohydrates_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.perc_carbohydrates_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.perc_carbohydrates_label, 4, 1)

        self.frame_2 = QFrame(self)
        self.frame_2.setMaximumHeight(150)
        self.grid.addWidget(self.frame_2, 1, 0)
        self.grid_2 = QGridLayout(self.frame_2)

        self.close_button = QPushButton('close window')
        self.close_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                        "border-radius: 20px;" +
                                        "font-size: 20px;" +
                                        "color: '#000000';" +
                                        "background: '#08fff0';" +
                                        "padding: 25px;}" +
                                        "*:hover{background: '#f8ff08';}"
                                        )
        self.close_button.clicked.connect(self.close)
        self.close_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.close_button.setMaximumWidth(250)
        self.grid_2.addWidget(self.close_button, 5, 1)

        self.calculate_macros()

        [item.setMaximumWidth(250) for item in [item for item in self.children() if type(
            item) not in [QGridLayout, QFrame]] if item != self.main_label]

    def calculate_macros(self):
        try:
            daily_intake = d.cursor.execute(
                f'SELECT * FROM "{d.formatted}"').fetchall()

            num_of_calories = sum([item[1] for item in daily_intake])
            if num_of_calories == 0:
                return
            total_calories = round(num_of_calories / 3000 * 100, 2)
            self.perc_total_label.setText(f'{total_calories} %')

            num_of_protein = round(
                sum([item[2] for item in daily_intake]) * 4 / num_of_calories * 100, 2)
            self.perc_protein_label.setText(f'{num_of_protein} %')

            num_of_fat = round(
                sum([item[3] for item in daily_intake]) * 9 / num_of_calories * 100, 2)
            self.perc_fat_label.setText(f'{num_of_fat} %')

            num_of_carbohydrates = round(
                sum([item[4] for item in daily_intake]) * 4 / num_of_calories * 100, 2)
            self.perc_carbohydrates_label.setText(f'{num_of_carbohydrates} %')
        except OperationalError:
            msg = QMessageBox(QMessageBox.Warning,
                              'No table found', f'No table for {d.formatted}')
            msg.exec_()


class NewFood(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle('New food entry')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.name_label = QLabel(self)
        self.name_label.setText('food name')
        self.name_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.name_label, 0, 0)

        self.total_label = QLabel(self)
        self.total_label.setText('calories')
        self.total_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.total_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.total_label, 1, 0)

        self.protein_label = QLabel(self)
        self.protein_label.setText('protein')
        self.protein_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.protein_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.protein_label, 2, 0)

        self.fat_label = QLabel(self)
        self.fat_label.setText('fat')
        self.fat_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.fat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.fat_label, 3, 0)

        self.carbohydrates_label = QLabel(self)
        self.carbohydrates_label.setText('carbohydrates')
        self.carbohydrates_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.carbohydrates_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.carbohydrates_label, 4, 0)

        self.food_name_edit = QLineEdit(self)
        self.food_name_edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                          "border-radius: 45px;" +
                                          "font-size: 25px;" +
                                          "padding: 0 25px;" +
                                          "color: '#000000';}")
        self.food_name_edit.setFocus()
        self.grid.addWidget(self.food_name_edit, 0, 1)

        self.calories_edit = QLineEdit(self)
        self.calories_edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                         "border-radius: 45px;" +
                                         "font-size: 25px;" +
                                         "padding: 0 25px;" +
                                         "color: '#000000';}")
        self.grid.addWidget(self.calories_edit, 1, 1)

        self.protein_edit = QLineEdit(self)
        self.protein_edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                        "border-radius: 45px;" +
                                        "font-size: 25px;" +
                                        "padding: 0 25px;" +
                                        "color: '#000000';}")
        self.grid.addWidget(self.protein_edit, 2, 1)

        self.fat_edit = QLineEdit(self)
        self.fat_edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                    "border-radius: 45px;" +
                                    "font-size: 25px;" +
                                    "padding: 0 25px;" +
                                    "color: '#000000';}")
        self.grid.addWidget(self.fat_edit, 3, 1)

        self.carbohydrates_edit = QLineEdit(self)
        self.carbohydrates_edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                              "border-radius: 45px;" +
                                              "font-size: 25px;" +
                                              "padding: 0 25px;" +
                                              "color: '#000000';}")
        self.grid.addWidget(self.carbohydrates_edit, 4, 1)

        self.insert_button = QPushButton('insert food')
        self.insert_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                         "border-radius: 20px;" +
                                         "font-size: 20px;" +
                                         "color: '#000000';" +
                                         "background: '#08fff0';" +
                                         "padding: 25px;}" +
                                         "*:hover{background: '#f8ff08';}"
                                         )
        self.insert_button.clicked.connect(self.insert_food)
        self.insert_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(self.insert_button, 5, 0)

        self.close_button = QPushButton('close window')
        self.close_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                        "border-radius: 20px;" +
                                        "font-size: 20px;" +
                                        "color: '#000000';" +
                                        "background: '#08fff0';" +
                                        "padding: 25px;}" +
                                        "*:hover{background: '#f8ff08';}"
                                        )
        self.close_button.clicked.connect(self.close)
        self.close_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.grid.addWidget(self.close_button, 5, 1)

        [item.setMaximumWidth(250)
         for item in self.children() if item != self.grid]

    def insert_food(self):
        food_name = self.food_name_edit.text()
        calories = self.calories_edit.text()
        protein = self.protein_edit.text()
        fat = self.fat_edit.text()
        carbohydrates = self.carbohydrates_edit.text()

        allowed_signs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']

        allowed = [item for item in (
            calories + protein + fat + carbohydrates) if item not in allowed_signs]
        if len(allowed) > 0:
            msg = QMessageBox(QMessageBox.Warning, 'Invalid number format',
                              'Please use only numbers separated be a decimal point when filling in nutrition info')
            msg.exec_()
            return

        if '' in [food_name, calories, protein, fat, carbohydrates]:
            msg = QMessageBox(QMessageBox.Warning, 'Missing information',
                              'Please fill in the remaining information')
            msg.exec_()
            return

        try:
            d.cursor.execute(
                f"INSERT INTO 'Foods' VALUES ('{food_name}', '{calories}', '{protein}', '{fat}', '{carbohydrates}')")
            d.db.commit()
        except IntegrityError:
            msg = QMessageBox(QMessageBox.Warning, 'Food already present',
                              f'Food {food_name} already present in Foods table')
            msg.exec_()

        self.food_name_edit.setText('')
        self.calories_edit.setText('')
        self.protein_edit.setText('')
        self.fat_edit.setText('')
        self.carbohydrates_edit.setText('')


class LookUpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle('Look up Window')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.frame_1 = QFrame(self)
        self.grid.addWidget(self.frame_1)

        self.grid_1 = QGridLayout(self.frame_1)

        self.total_label = QLabel(self.frame_1)
        self.total_label.setText('calories')
        self.total_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.total_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.total_label, 0, 0)

        self.protein_label = QLabel(self.frame_1)
        self.protein_label.setText('protein')
        self.protein_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.protein_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.protein_label, 1, 0)

        self.fat_label = QLabel(self.frame_1)
        self.fat_label.setText('fat')
        self.fat_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.fat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.fat_label, 2, 0)

        self.carbohydrates_label = QLabel(self.frame_1)
        self.carbohydrates_label.setText('carbohydrates')
        self.carbohydrates_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.carbohydrates_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.carbohydrates_label, 3, 0)

        self.total_kcal_label = QLabel(self.frame_1)
        self.total_kcal_label.setText('0 g')
        self.total_kcal_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.total_kcal_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.total_kcal_label, 0, 1)

        self.protein_g_label = QLabel(self.frame_1)
        self.protein_g_label.setText('0 g')
        self.protein_g_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.protein_g_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.protein_g_label, 1, 1)

        self.fat_g_label = QLabel(self.frame_1)
        self.fat_g_label.setText('0 g')
        self.fat_g_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.fat_g_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.fat_g_label, 2, 1)

        self.carbohydrates_g_label = QLabel(self.frame_1)
        self.carbohydrates_g_label.setText('0 g')
        self.carbohydrates_g_label.setStyleSheet(
            'color: 000000;' + "font-size: 25px")
        self.carbohydrates_g_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_1.addWidget(self.carbohydrates_g_label, 3, 1)

        self.name_edit = QLineEdit(self)
        self.name_edit.setStyleSheet("*{border: 4px solid '#000000';" +
                                     "border-radius: 45px;" +
                                     "font-size: 25px;" +
                                     "padding: 0 25px;" +
                                     "color: '#000000';}")
        self.name_edit.setMaximumWidth(250)
        self.grid_1.addWidget(self.name_edit, 4, 0)

        self.close_button = QPushButton('search database')
        self.close_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                        "border-radius: 20px;" +
                                        "font-size: 20px;" +
                                        "color: '#000000';" +
                                        "background: '#08fff0';" +
                                        "padding: 25px;}" +
                                        "*:hover{background: '#f8ff08';}"
                                        )
        self.close_button.clicked.connect(self.calculate_macros)
        self.close_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.grid_1.addWidget(self.close_button, 4, 1)

        self.frame_2 = QFrame(self)
        self.frame_2.setMaximumHeight(150)
        self.grid.addWidget(self.frame_2, 1, 0)
        self.grid_2 = QGridLayout(self.frame_2)

        self.close_button = QPushButton('close window')
        self.close_button.setStyleSheet("*{border: 4px solid '#000000';" +
                                        "border-radius: 20px;" +
                                        "font-size: 20px;" +
                                        "color: '#000000';" +
                                        "background: '#08fff0';" +
                                        "padding: 25px;}" +
                                        "*:hover{background: '#f8ff08';}"
                                        )
        self.close_button.clicked.connect(self.close)
        self.close_button.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.grid_2.addWidget(self.close_button, 5, 1)

        [item.setMaximumWidth(250) for item in (
            self.frame_1.children() + self.frame_2.children()) if type(item) != QGridLayout]

    def calculate_macros(self):
        food = self.name_edit.text()
        macros = d.cursor.execute(
            f'SELECT * FROM "Foods" WHERE food_name = "{food}"').fetchall()
        if len(macros) == 0:
            msg = QMessageBox(QMessageBox.Warning,
                              'Food not found', 'Food not found')
            msg.exec_()
            return

        self.total_kcal_label.setText(f'{macros[0][1]} kcal')

        self.protein_g_label.setText(f'{macros[0][2]} g')

        self.fat_g_label.setText(f'{macros[0][3]} g')

        self.carbohydrates_g_label.setText(f'{macros[0][4]} g')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = DietingApp()
    d.show()
    app.exec()
