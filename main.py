from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5.QtWidgets import QGraphicsScene, QInputDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from random import sample
import sys
import os.path
import csv


STRAPS_LIST = ["Рядовой", "Ефрейтор", "Младший сержант", "Сержант", "Старший Сержант", "Старшина", "Прапорщик",
               "Старший Прапорщик", "Младший Лейтенант", "Лейтенант", "Старший Лейтенант", "Капитан", "Майор",
               "Подполковник", "Полковник", "Генерал-Майор", "Генерал-Лейтенант", "Генерал-Полковник", "Генерал Армии",
               "Маршал РФ"]
STRAPS_IMAGES_DIR = "Images"
STRAPS_NUM = 10

UI_FILENAME = "StrapsMainWindow.ui"

RESULTS_FILENAME = "Результаты.csv"


class StrapsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILENAME, self)

        self.window_definition()
        self.calls_processing()

        self.current_question = 0
        self.right_answers = 0
        self.form = None
        self.straps = None

    def window_definition(self):
        self.tabWidget.setTabVisible(0, False)
        self.refresh_table()

    def calls_processing(self):
        self.addFormAction.triggered.connect(self.add_form)
        self.answerButton.clicked.connect(self.get_answer)
        self.deleteRusultsButton.clicked.connect(self.erase_results)

    def erase_results(self):
        if os.path.exists(RESULTS_FILENAME):
            os.remove(RESULTS_FILENAME)
        self.refresh_table()

    def add_form(self):
        self.form, ok = QInputDialog.getText(self, "Добавление класса", "Введите класс:")
        if ok:
            self.first_tab_refresh()

    def refresh_table(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        if os.path.exists(RESULTS_FILENAME):
            with open(RESULTS_FILENAME, encoding="UTF-8") as res_f:
                data = []
                reader = csv.reader(res_f, delimiter=";")
                for form_data in reader:
                    data.append(form_data)
            data.sort(key=lambda row_values: row_values[1], reverse=True)

            self.tableWidget.setHorizontalHeaderLabels(["Класс", "Результат"])
            self.tableWidget.setRowCount(len(data))
            for row, (form, res) in enumerate(data):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(form))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(res))
        else:
            self.tableWidget.setHorizontalHeaderLabels(["Грустно", "Пусто :("])

    def fill_table(self):
        with open(RESULTS_FILENAME, "a", encoding="UTF-8", newline="") as res_f:
            writer = csv.writer(res_f, delimiter=";")
            writer.writerow([self.form, self.right_answers])
        self.refresh_table()

    def first_tab_refresh(self):
        self.tabWidget.setCurrentIndex(0)
        self.formLabel.setText(self.form)

        self.strapsComboBox.clear()
        self.strapsComboBox.addItems(STRAPS_LIST)

        self.current_question = 0
        self.right_answers = 0

        self.progressBar.setValue(self.current_question)
        self.tabWidget.setTabVisible(0, True)
        self.answerButton.setEnabled(True)

        self.straps = sample(STRAPS_LIST, STRAPS_NUM)
        self.change_image()

    def change_image(self):
        straps_name = self.straps[self.current_question]
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap(STRAPS_IMAGES_DIR + "/" + straps_name + ".jpg"))
        self.graphicsView.setScene(scene)

    def get_answer(self):
        if self.strapsComboBox.currentText() == self.straps[self.current_question]:
            self.right_answers += 1
            self.statusBar().showMessage("Верно.", 3000)
        else:
            self.statusBar().showMessage("Неверно.", 3000)

        self.current_question += 1
        self.progressBar.setValue(self.current_question)

        if self.current_question == STRAPS_NUM:
            self.ending()
        else:
            self.change_image()

    def ending(self):
        self.answerButton.setEnabled(False)
        QMessageBox.about(self, "Тест окончен",
                          f"Вы набрали {self.right_answers} из {STRAPS_NUM} баллов!")
        self.fill_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StrapsMainWindow()
    window.show()
    sys.exit(app.exec())
