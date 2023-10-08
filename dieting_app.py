from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QFrame, QLineEdit, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
from sqlite3 import IntegrityError, OperationalError
from datetime import datetime
import numpy as np
import sqlite3
import sys

matplotlib.use('Qt5Agg')


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

        self.grid.addWidget(MainLabel('Dieting app'), 0, 1)

        self.food_button = PushButton('new entry', self.new_entry)
        self.grid.addWidget(self.food_button, 1, 0)

        self.macros_button = PushButton('macros window', self.macros_window)
        self.grid.addWidget(self.macros_button, 1, 1)

        self.new_food_button = PushButton('new food type', self.new_food_type)
        self.grid.addWidget(self.new_food_button, 1, 2)

        self.close_app_button = PushButton('close app', self.close_app)
        self.grid.addWidget(self.close_app_button, 2, 1)

    def new_entry(self):
        self.new_window = NewEntry()
        self.new_window.show()

    def macros_window(self):
        self.new_window = Macros()
        self.new_window.show()

    def new_food_type(self):
        self.new_window = NewFood()
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
        self.setGeometry(0, 0, 800, 700)
        self.setWindowTitle('Food entry')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.frame_1 = QFrame(self)
        self.grid.addWidget(self.frame_1, 1, 0)
        self.grid_1 = QGridLayout(self.frame_1)

        self.food_name_label = Label('food name')
        self.grid_1.addWidget(self.food_name_label, 0, 0)

        self.food_name_edit = UserLineEdit(True)
        self.grid_1.addWidget(self.food_name_edit, 1, 0)

        self.food_quantity_label = Label('food quantity (g)')
        self.grid_1.addWidget(self.food_quantity_label, 2, 0)

        self.food_quantity_edit = UserLineEdit()
        self.grid_1.addWidget(self.food_quantity_edit, 3, 0)

        self.add_button = PushButton('add a food', self.add_food)
        self.grid_1.addWidget(self.add_button, 0, 1)

        self.remove_button = PushButton('remove a food', self.remove_food)
        self.grid_1.addWidget(self.remove_button, 1, 1)

        self.clear_button = PushButton('clear plan', self.clear_plan)
        self.grid_1.addWidget(self.clear_button, 2, 1)

        self.select_button = PushButton('select a food', self.select_food)
        self.grid_1.addWidget(self.select_button, 3, 1)

        self.close_button = PushButton('close window', self.close)
        self.grid_1.addWidget(self.close_button, 4, 1)

        self.frame_2 = QFrame(self)
        self.grid.addWidget(self.frame_2, 0, 0)
        self.grid_2 = QGridLayout(self.frame_2)

        self.total_label = Label('total calories')
        self.grid_2.addWidget(self.total_label, 1, 0)

        self.protein_label = Label('total protein')
        self.grid_2.addWidget(self.protein_label, 2, 0)

        self.fat_label = Label('total fat')
        self.grid_2.addWidget(self.fat_label, 3, 0)

        self.carbohydrates_label = Label('total carbohydrates')
        self.grid_2.addWidget(self.carbohydrates_label, 4, 0)

        self.num_total_label = Label('0 kcal')
        self.grid_2.addWidget(self.num_total_label, 1, 1)

        self.num_protein_label = Label('0 g')
        self.grid_2.addWidget(self.num_protein_label, 2, 1)

        self.num_fat_label = Label('0 g')
        self.grid_2.addWidget(self.num_fat_label, 3, 1)

        self.num_carbohydrates_label = Label('0 g')
        self.grid_2.addWidget(self.num_carbohydrates_label, 4, 1)

        try:
            self.insert_data()
        except OperationalError:
            pass

        [item.setMaximumWidth(250) for item in self.frame_1.children() if type(
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

        self.remove = RemoveFood()
        self.remove.show()

        if 0 == 1:

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


class RemoveFood(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 800, 700)
        self.setWindowTitle('Remove food window')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.frame_1 = QFrame(self)
        self.grid_1 = QGridLayout(self.frame_1)

        self.grid.addWidget(self.frame_1, 0, 0)

        self.frame_2 = QFrame(self)
        self.grid_2 = QGridLayout(self.frame_2)

        self.grid.addWidget(self.frame_2, 1, 0)

        self.close_button = PushButton('Close window', self.close)
        self.close_button.setMaximumWidth(250)
        self.grid_2.addWidget(self.close_button, 0, 0)

        self.formatted = datetime.now().strftime("%Y-%m-%d")

        self.today = d.cursor.execute(
            f'SELECT * FROM "{d.formatted}"').fetchall()

        self.buttons = []

        self.row = 0
        column = 0

        for food in self.today:
            button = PushButton(f'{food[0]}', self.delete_food)
            button.setMaximumWidth(250)
            self.buttons.append(button)
            self.grid_1.addWidget(button, self.row, column)
            column += 1
            if column != 0:
                if column % 5 == 0:
                    self.row += 1
                    column = 0

    def delete_food(self):
        text = self.sender().text()
        self.sender().hide()

        d.cursor.execute(
            f'DELETE FROM "{d.formatted}" WHERE food_name = "{text}"')
        d.db.commit()

        d.new_window.insert_data()


class SelectFood(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 600, 400)
        self.setWindowTitle('Select a food')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.buttons = []

        self.get_foods()

        self.label = Label('Search for food: ')
        self.grid.addWidget(self.label, self.row + 1, 0)

        self.edit = TextEdit()

        self.edit.setFocus()
        self.edit.textEdited.connect(self.filter_foods)
        self.grid.addWidget(self.edit, self.row + 1, 1)

    def get_foods(self):
        foods = [item[0] for item in d.cursor.execute(
            'SELECT food_name FROM foods').fetchall()]
        self.row = 0
        column = 0
        for food in foods:
            button = PushButton(f'{food}', self.add_text)
            button.setMaximumWidth(250)
            self.buttons.append(button)
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


class Macros(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle('Macros window')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.frame_1 = QFrame(self)
        self.frame_1.setMinimumHeight(300)
        self.grid.addWidget(self.frame_1)

        self.grid_1 = QGridLayout(self.frame_1)

        self.main_label = MainLabel('macros distribution')
        self.grid_1.addWidget(self.main_label, 0, 0, 1, 2)

        self.total_label = Label('Num of calories')
        self.grid_1.addWidget(self.total_label, 1, 0)

        self.protein_label = Label('Num of protein')
        self.grid_1.addWidget(self.protein_label, 2, 0)

        self.perc_total_label = Label('0')
        self.grid_1.addWidget(self.perc_total_label, 1, 1)

        self.perc_protein_label = Label('0')
        self.grid_1.addWidget(self.perc_protein_label, 2, 1)

        self.frame_2 = QFrame(self)
        self.grid.addWidget(self.frame_2, 1, 0)
        self.grid_2 = QGridLayout(self.frame_2)

        self.frame_3 = QFrame(self)
        self.grid.addWidget(self.frame_3, 2, 0)
        self.grid_3 = QGridLayout(self.frame_3)

        self.change_button = PushButton('Change values', self.change_values)
        self.change_button.setMaximumWidth(250)
        self.grid_3.addWidget(self.change_button, 0, 0)

        self.close_button = PushButton('close window', self.close)
        self.close_button.setMaximumWidth(250)
        self.grid_3.addWidget(self.close_button, 0, 1)

        self.total_calories = int(d.cursor.execute(
            'SELECT calorie_goal FROM goals').fetchall()[0][0])
        self.total_protein = int(d.cursor.execute(
            'SELECT protein_goal FROM goals').fetchall()[0][0])

        [item.setMaximumWidth(250) for item in [item for item in self.children() if type(
            item) not in [QGridLayout, QFrame]] if item != self.main_label]

        self.calculate_macros()

    def calculate_macros(self):
        try:
            daily_intake = d.cursor.execute(
                f'SELECT * FROM "{d.formatted}"').fetchall()

            num_of_calories = sum([item[1] for item in daily_intake])
            num_of_protein = sum(item[2] for item in daily_intake)

            if num_of_calories == 0:
                return

            total_calories = round(
                num_of_calories / self.total_calories * 100, 2)

            self.perc_total_label.setText(
                f'{num_of_calories} / {self.total_calories}, {total_calories} %')

            self.perc_protein_label.setText(
                f'{num_of_protein} / {self.total_protein}, {num_of_protein} %')

            num_of_protein = round(
                sum([item[2] for item in daily_intake]) * 4 / num_of_calories * 100, 2)

            num_of_fat = round(
                sum([item[3] for item in daily_intake]) * 9 / num_of_calories * 100, 2)

            num_of_carbohydrates = round(
                sum([item[4] for item in daily_intake]) * 4 / num_of_calories * 100, 2)

            self.macros = ['protein', 'fat', 'carbohydrate']
            self.amounts = [num_of_protein, num_of_fat, num_of_carbohydrates]

            self.pie = MplCanvasPie(self, width=6, height=10, dpi=100)
            self.pie.show_overview(amounts=self.amounts, assets=self.macros)
            self.grid_2.addWidget(self.pie, 0, 0)

        except OperationalError:
            msg = QMessageBox(QMessageBox.Warning,
                              'No table found', f'No table for {d.formatted}')
            msg.exec_()

    def change_values(self):

        self.change = ChangeWindow()
        self.change.show()


class ChangeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle('Change caloric and protein goals window')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)
        self.frame_1 = QFrame(self)
        self.frame_2 = QFrame(self)

        self.grid_1 = QGridLayout(self.frame_1)
        self.grid_2 = QGridLayout(self.frame_2)

        self.grid.addWidget(self.frame_1, 0, 0)
        self.grid.addWidget(self.frame_2, 1, 0)

        self.grid_1.addWidget(Label('Current calorie goal'), 0, 0)
        self.total_kc = Label(str(d.new_window.total_calories))
        self.grid_1.addWidget(self.total_kc, 0, 1)
        self.grid_1.addWidget(Label('New calorie goal'), 1, 0)

        self.kcal_edit = UserLineEdit()
        self.grid_1.addWidget(self.kcal_edit, 1, 1)
        self.kcal_button = PushButton('Change calories', self.change_calories)
        self.grid_1.addWidget(self.kcal_button, 1, 2)

        self.grid_2.addWidget(Label('Current protein goal'), 0, 0)
        self.total_pr = Label(str(d.new_window.total_protein))
        self.grid_2.addWidget(self.total_pr, 0, 1)
        self.grid_2.addWidget(Label('New protein goal'), 1, 0)

        self.prot_edit = UserLineEdit()
        self.grid_2.addWidget(self.prot_edit, 1, 1)
        self.prot_button = PushButton('Change protein', self.change_protein)
        self.grid_2.addWidget(self.prot_button, 1, 2)

    def change_calories(self):
        self.total_kc.setText(self.kcal_edit.text())
        d.cursor.execute(
            f'UPDATE goals SET calorie_goal = "{self.kcal_edit.text()}"')
        d.new_window.total_calories = int(self.kcal_edit.text())
        d.new_window.calculate_macros()
        self.kcal_edit.clear()
        d.db.commit()

    def change_protein(self):
        self.total_pr.setText(self.prot_edit.text())
        d.cursor.execute(
            f'UPDATE goals SET protein_goal = "{self.prot_edit.text()}"')
        d.new_window.total_protein = int(self.prot_edit.text())
        d.new_window.calculate_macros()
        self.prot_edit.clear()
        d.db.commit()


class NewFood(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle('New food entry')
        self.setStyleSheet('background: #ffffff')

        self.grid = QGridLayout(self)

        self.name_label = Label('food name')
        self.grid.addWidget(self.name_label, 0, 0)

        self.total_label = Label('calories')
        self.grid.addWidget(self.total_label, 1, 0)

        self.protein_label = Label('protein')
        self.grid.addWidget(self.protein_label, 2, 0)

        self.fat_label = Label('fat')
        self.grid.addWidget(self.fat_label, 3, 0)

        self.carbohydrates_label = Label('carbohydrates')
        self.grid.addWidget(self.carbohydrates_label, 4, 0)

        self.food_name_edit = UserLineEdit(self)
        self.grid.addWidget(self.food_name_edit, 0, 1)

        self.calories_edit = UserLineEdit(self)
        self.grid.addWidget(self.calories_edit, 1, 1)

        self.protein_edit = UserLineEdit(self)
        self.grid.addWidget(self.protein_edit, 2, 1)

        self.fat_edit = UserLineEdit()
        self.grid.addWidget(self.fat_edit, 3, 1)

        self.carbohydrates_edit = UserLineEdit()
        self.grid.addWidget(self.carbohydrates_edit, 4, 1)

        self.insert_button = PushButton('insert food', self.insert_food)
        self.grid.addWidget(self.insert_button, 5, 0)

        self.close_button = PushButton('close window', self.close)
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


class Label(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet('color: 000000;' + "font-size: 25px")
        self.setAlignment(QtCore.Qt.AlignCenter)


class MainLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet('color: 000000;' + "font-size: 50px")
        self.setAlignment(QtCore.Qt.AlignCenter)


class PushButton(QPushButton):
    def __init__(self, text, function):
        super().__init__()
        self.setText(text)
        self.setStyleSheet("*{border: 4px solid '#000000';" +
                           "border-radius: 45px;" +
                           "font-size: 30px;" +
                           "color: '#000000';" +
                           "background: '#08fff0';" +
                           "padding: 25px;}" +
                           "*:hover{background: '#f8ff08';}"
                           )
        self.setCursor(
            QCursor(QtCore.Qt.PointingHandCursor))
        self.clicked.connect(function)


class UserLineEdit(QLineEdit):
    def __init__(self, focus=False, width=False):
        super().__init__()
        self.setStyleSheet("*{border: 4px solid '#000000';" +
                           "border-radius: 45px;" +
                           "font-size: 25px;" +
                           "padding: 0 25px;" +
                           "color: '#000000';}")
        if focus:
            self.setFocus()

        if width:
            self.setMaximumWidth(width)


class TextEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("*{border: 4px solid '#000000';" +
                           "border-radius: 45px;" +
                           "font-size: 25px;" +
                           "padding: 0 25px;" +
                           "color: '#000000';}")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            try:
                d.new_window.select.edit.setText(
                    d.new_window.select.edit.text()[:-1])
                d.new_window.select.filter_foods()
                d.new_window.select.show_buttons()
            except IndexError:
                pass
        super(TextEdit, self).keyPressEvent(event)


class MplCanvasPie(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvasPie, self).__init__(fig)

    def show_overview(self, amounts, assets):
        def func(pct, allvals):
            absolute = int(np.round(pct/100.*np.sum(allvals)))
            return "{:.1f}%\n".format(pct, absolute)

        wedges, texts, autotexts = self.axes.pie(amounts, autopct=lambda pct: func(pct, amounts),
                                                 textprops=dict(color="w"))

        self.axes.legend(wedges, assets,
                         title='Macros',
                         loc="lower right",
                         bbox_to_anchor=(0, 0, 0, 0))

        plt.setp(autotexts, size=8, weight="bold")

        self.axes.set_title(f'Macros distribution for today: ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = DietingApp()
    d.show()
    app.exec()
