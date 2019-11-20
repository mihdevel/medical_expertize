from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication,
                             QPushButton, QLabel, QLineEdit,
                             QComboBox, QTableWidget,
                             QTableWidgetItem, QSlider)


class baseWidets:
    """docstring for ContoursProcess"""

    def __init__(self):
        pass

    def label(self, text=None):
        return QLabel(text)

    def button(self, text):
        return QPushButton(text)

    def lineEdit(self):
        return QLineEdit()

    def list(self, items):
        list = QComboBox()
        list.addItems(items)
        return list

    def table(self, row=None, column=None):
        table = QTableWidget()
        table.setRowCount(row or 1)
        table.setColumnCount(column or 1)
        return table


if __name__ == "__main__":

    class Main(QLabel, baseWidets):
        def __init__(self):
            super().__init__()
            self.initStartUi()


        def initStartUi(self):
            self.grid = QGridLayout()
            self.setLayout(self.grid)
            self.setWindowTitle('Выбор действий')
            self.setGeometry(500, 300, 10, 10)
            self.grid.setSpacing(10)

            self.grid.addWidget(self.button('Калибровка'), 0, 0)
            self.grid.addWidget(self.button('Измерение'), 0, 1)
            self.grid.addWidget(self.table(2, 3), 1, 1)
            self.show()


    import sys

    app = QApplication(sys.argv)
    Main()
    sys.save(app.exec_())