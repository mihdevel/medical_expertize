import sys
from PyQt5.QtWidgets import QGridLayout, QApplication, QLabel,\
                            QWidget, QDesktopWidget

from mainWindow import MainWindow
from guimixin import *

class Main(MainWindow, GuiMixin):
    """docstring for Main"""

    def __init__(self):
        super().__init__()

        # self.getPicture()
        self.data = []

        # self.start()

    def start(self):
        pass

    def proc(self):
        self.filename = 'process/test-2-2.png'
        self.name_file_img_with_counturs = 'process/img_with_counturs.png'

        # self.getPicture()
        self.imgShow()

        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.valueChanged[int].connect(self.changeSlider)

        self.scanFotoBtn.clicked[bool].connect(self.getPicture)
        self.fixBtn.clicked[bool].connect(self.fixMode)
        self.processBtn.clicked[bool].connect(self.calculateResult)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())