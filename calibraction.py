from PyQt5.QtGui import QIntValidator#, QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QApplication, QLabel,\
                            QWidget, QDesktopWidget, QTableWidgetItem

from basewidgets import baseWidets
from scanCalibraction import ScanColibration

class Calibration(QLabel, baseWidets):
    """docstring for Calibration"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent or self
        self.calibration_ui()

    def calibration_ui(self):
        self.win_calibration = QWidget(self.parent, Qt.Window)
        self.win_calibration.setWindowModality(Qt.WindowModal)
        self.win_calibration.setGeometry(100, 100, 950, 350)
        self.win_calibration.setWindowTitle('Калибровка')

        self.win_calibration.grid = QGridLayout()
        self.win_calibration.setLayout(self.win_calibration.grid)

        lbl_organization = self.label('Организация')
        self.qle_organization = self.lineEdit()

        lbl_position = self.label('Должность')
        self.qle_position = self.lineEdit()

        lbl_fullName = self.label('ФИО')
        self.qle_fullName = self.lineEdit()

        lbl_phone = self.label('Телефон')
        self.qle_phone = self.lineEdit()
        self.qle_phone.setInputMask('+7-999-999-99-99')

        lbl_lot_number = self.label('Номер партии теста')
        self.qle_lot_number = self.lineEdit()
        self.qle_lot_number.setValidator(QIntValidator())

        lbl_shelf_life = self.label('Срок годности')
        self.qle_shelf_life = self.lineEdit()
        self.qle_shelf_life.setInputMask('99.99.9999')

        lbl_test_type = self.label('Тип теста')
        self.combo_test_type = self.list(["Amylase",
                                     "HemDirect", "PSA_Semiquant"])

        lbl_number_measurement_points = self.label('Колличество точек измерения')
        # lblNumberMeasurementPoints = self.label('Колличество точек')
        self.combo_number_measurement_points = self.list(["5", "6",
                                            "7", "8", "9"])
        self.combo_number_measurement_points.activated[str].connect(self.change_count_table_columns)

        lbl_units = self.label('Единицы измерения')
        self.combo_units = self.list(["ng/ml",
                                  "mg/ml", "mME/ml"])
        self.combo_units.activated[str].connect(self.draw_header_labels)

        # measurement_points = int(comboNumberMeasurementPoints.currentText())
        self.table_use = self.table()
        self.draw_table(1, 5)

        # self.table_use.setItem(0, 0, QTableWidgetItem("1, 1"))
        # win_calibration.table.move(0, 0)

        btn_save = self.button('Сохранить результаты')
        btn_save.clicked[bool].connect(self.save_result)


        self.win_calibration.grid.addWidget(lbl_organization, 0, 0)
        self.win_calibration.grid.addWidget(self.qle_organization, 1, 0)

        self.win_calibration.grid.addWidget(lbl_position, 0, 1)
        self.win_calibration.grid.addWidget(self.qle_position, 1, 1)

        self.win_calibration.grid.addWidget(lbl_fullName, 0, 2)
        self.win_calibration.grid.addWidget(self.qle_fullName, 1, 2)

        self.win_calibration.grid.addWidget(lbl_phone, 0, 3)
        self.win_calibration.grid.addWidget(self.qle_phone, 1, 3)

        self.win_calibration.grid.addWidget(lbl_lot_number, 2, 0)
        self.win_calibration.grid.addWidget(self.qle_lot_number, 3, 0)

        self.win_calibration.grid.addWidget(lbl_shelf_life, 2, 1)
        self.win_calibration.grid.addWidget(self.qle_shelf_life, 3, 1)

        self.win_calibration.grid.addWidget(lbl_test_type, 2, 2)
        self.win_calibration.grid.addWidget(self.combo_test_type, 3, 2)

        self.win_calibration.grid.addWidget(lbl_number_measurement_points, 2, 3)
        self.win_calibration.grid.addWidget(self.combo_number_measurement_points, 3, 3)

        self.win_calibration.grid.addWidget(lbl_units, 2, 4)
        self.win_calibration.grid.addWidget(self.combo_units, 3, 4)

        self.win_calibration.grid.addWidget(self.table_use, 4, 0, 4, 5)

        self.win_calibration.grid.addWidget(btn_save, 8, 4)
        # self.win_calibration.show()

    def draw_table(self, row=None, column=None):
        # assert isinstance(int(column or self.combo_number_measurement_points.currentText()), int)
        self.column = int(column or self.combo_number_measurement_points.currentText())

        self.row = int(row) or 1
        self.table_use.setRowCount(self.row)
        self.table_use.setColumnCount(self.column)
        self.draw_header_labels()

        for i in range(0, self.column):
            self.btn_scan = self.button('Сканировать')
            self.btn_scan.setObjectName("button_" + str(i))
            self.btn_scan.clicked[bool].connect(self.open_scaning_colibration_win)
            self.table_use.setCellWidget(self.row - 1, i, self.btn_scan)

    def change_count_table_columns(self):
        self.draw_table(1, self.combo_number_measurement_points.currentText())

    def draw_header_labels(self):
        self.table_use.setHorizontalHeaderLabels([str(x) + ' ' + self.combo_units.currentText() for x in range(5, 50, 5)])

    def save_result(self):
        import xml.etree.ElementTree as ET
        import datetime

        # tree = ET.parse('colibration/PSA_F14074_SQ201.xml')
        tree = ET.parse('colibration/PSA_Template.xml')
        root = tree.getroot()

        description = ET.Element("description")
        description.text = 'PSA Calibration Curve SQ201'

        organization = ET.Element("organization")
        organization.text = self.qle_organization.text()

        position = ET.Element("position")
        position.text = self.qle_position.text()

        full_name = ET.Element("name")
        full_name.text = self.qle_fullName.text()

        phone = ET.Element("phone")
        phone.text = self.qle_phone.text()

        operator = ET.Element("operator")
        operator.insert(0, organization)
        operator.insert(1, position)
        operator.insert(2, full_name)
        operator.insert(3, phone)

        created_by = ET.Element("created_by")
        created_by.insert(0, operator)

        shelf_life = ET.Element("shelf_life")
        shelf_life.text = self.qle_shelf_life.text()

        point = ET.Element("point")
        point.set("x", "value")
        point.set("mean", "value")
        point.set("var", "value")
        point.set("skew", "value")
        point.set("reliability", "value")
        point.set("samples-used", "value")

        calibration_data = ET.Element("calibration_data")
        calibration_data.insert(0, point)

        root.insert(0, description)
        root.insert(1, created_by)
        root.insert(8, calibration_data)
        root.insert(9, shelf_life)

        # print(root.find('description').text)
        # tree = ET.ElementTree(root)

        test_type = self.combo_test_type.currentText()
        lot_number = self.qle_lot_number.text()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        output_name_file_xml = "{}_{}_{}.xml".format(test_type, lot_number, current_date)

        tree.write("colibration/" + output_name_file_xml)

        self.win_calibration.deleteLater()

    def open_scaning_colibration_win(self):
        scaning_colibration_win = ScanColibration(self)
        scaning_colibration_win.win_scan_calibration.show()