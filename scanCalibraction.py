from PyQt5.QtGui import QPixmap, QIntValidator#, QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QApplication, QLabel,\
                            QWidget, QDesktopWidget, QTableWidgetItem

from basewidgets import baseWidets

class ScanColibration(QLabel, baseWidets):
    """docstring for ScanColibration"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent or self
        self.scan_colibration_ui()
        # print(self.parent.btn_scan.objectName())

    def scan_colibration_ui(self):
        self.win_scan_calibration = QWidget(self.parent, Qt.Window)
        self.win_scan_calibration.setWindowModality(Qt.WindowModal)
        self.win_scan_calibration.setGeometry(100, 100, 600, 500)
        self.win_scan_calibration.setWindowTitle('Cканивание калибровки')

        self.win_scan_calibration.grid = QGridLayout()
        self.win_scan_calibration.setLayout(self.win_scan_calibration.grid)

        btn_calculation = self.button('Расчет')
        btn_calculation.clicked[bool].connect(self.calculate_calibration)
        btn_exit = self.button('Выход')
        btn_exit.clicked[bool].connect(self.exit)

        field_img = self.label()
        field_img.setPixmap(QPixmap('foto-tester/test-3.png'))

        self.win_scan_calibration.grid.addWidget(field_img, 0, 0, 4, 4)
        self.win_scan_calibration.grid.addWidget(btn_exit, 3, 2)
        self.win_scan_calibration.grid.addWidget(btn_calculation, 3, 3)

        self.win_scan_calibration.show()
        # print(self.parent.scaning.objectName())

    def calculate_calibration(self):
        self.parent.draw_table(2, 5)
        # self.parent.table_use.setItem(0, 0, QTableWidgetItem("1, 1"))
        # self.addTableColumnValue(0, 0, 'Yes')
        # self.win_scan_calibration.deleteLater()

    def exit(self):
        self.win_scan_calibration.deleteLater()