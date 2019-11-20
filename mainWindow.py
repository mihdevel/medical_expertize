from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QApplication, QLabel,\
                            QWidget, QDesktopWidget

from basewidgets import baseWidets
from calibraction import Calibration
from scanCalibraction import ScanColibration
from measurement import Measurement

class MainWindow(QLabel, baseWidets):
    """docstring for MainWindow"""

    def __init__(self):
        super().__init__()
        self.main_window_ui()
        self.main_window.show()

    def main_window_ui(self):
        self.main_window = QWidget(self, Qt.Window)
        self.main_window.setWindowModality(Qt.WindowModal)
        self.main_window.setGeometry(400, 400, 20, 20)
        self.main_window.setWindowTitle('Главная')

        self.main_window.grid = QGridLayout()
        self.main_window.setLayout(self.main_window.grid)

        calibration = self.button('Калибровка')
        mesurement = self.button('Измерение')

        calibration.clicked[bool].connect(self.open_calibration_win)
        mesurement.clicked[bool].connect(self.open_mesurement_win)

        self.main_window.grid.addWidget(calibration, 0, 0)
        self.main_window.grid.addWidget(mesurement, 0, 1)

        # self.main_window.show()

    def open_calibration_win(self):
        calibration_win = Calibration(self.main_window)
        calibration_win.win_calibration.show()

    def open_mesurement_win(self):
        mesurement_win = Measurement(self.main_window)
        mesurement_win.win_mesurement.show()
