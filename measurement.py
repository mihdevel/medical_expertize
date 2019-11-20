import os
import re
import pydf
from PyQt5.QtGui import QPixmap, QIntValidator#, QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QApplication, QLabel,\
                            QWidget, QDesktopWidget, QFileDialog

from basewidgets import baseWidets
from guimixin import GuiMixin


class Measurement(QLabel, baseWidets):
    """docstring for Measurement"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent or self
        self.measurement_ui()

    def measurement_ui(self):
        self.win_mesurement = QWidget(self.parent, Qt.Window)
        self.win_mesurement.setWindowModality(Qt.WindowModal)
        self.win_mesurement.setGeometry(100, 100, 900, 600)
        self.win_mesurement.setWindowTitle('Измерение')
        self.win_mesurement.grid = QGridLayout()
        self.win_mesurement.setLayout(self.win_mesurement.grid)

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

        lbl_file_colibration = self.label('Файл калибровки')
        file_name_colibration = self.found_files_colibration()
        if not file_name_colibration:
            self.field_file_colibration = self.button('Выбрать файл калибровки')
            self.field_file_colibration.clicked[bool].connect(self.get_file)
        else:
            self.field_file_colibration = self.list(file_name_colibration)

        lbl_description = self.label('Примечание')
        qle_description = self.lineEdit()


        self.opencv = GuiMixin('process/test-3.png')
        # self.opencv = GuiMixin('process/test-2-2.png')
        filename = self.opencv.name_file_img_with_counturs
        # filename = self.opencv.name_file_img_with_counturs

        field_img = self.label()
        field_img.setPixmap(QPixmap(filename))
        # field_img.setPixmap(QPixmap('foto-tester/test-3.png'))

        btn_rescan = self.button('Рескан')
        self.lbl_result = self.label('Результат')
        btn_accept = self.button('Принять')

        btn_rescan.clicked[bool].connect(self.rescan)
        btn_accept.clicked[bool].connect(self.save)

        self.win_mesurement.grid.addWidget(lbl_organization, 0, 0)
        self.win_mesurement.grid.addWidget(self.qle_organization, 1, 0)

        self.win_mesurement.grid.addWidget(lbl_position, 0, 1)
        self.win_mesurement.grid.addWidget(self.qle_position, 1, 1)

        self.win_mesurement.grid.addWidget(lbl_fullName, 0, 2)
        self.win_mesurement.grid.addWidget(self.qle_fullName, 1, 2)

        self.win_mesurement.grid.addWidget(lbl_phone, 0, 3)
        self.win_mesurement.grid.addWidget(self.qle_phone, 1, 3)

        self.win_mesurement.grid.addWidget(lbl_lot_number, 2, 0)
        self.win_mesurement.grid.addWidget(self.qle_lot_number, 3, 0)

        self.win_mesurement.grid.addWidget(lbl_shelf_life, 2, 1)
        self.win_mesurement.grid.addWidget(self.qle_shelf_life, 3, 1)

        self.win_mesurement.grid.addWidget(lbl_test_type, 2, 2)
        self.win_mesurement.grid.addWidget(self.combo_test_type, 3, 2)

        self.win_mesurement.grid.addWidget(lbl_file_colibration, 2, 3)
        self.win_mesurement.grid.addWidget(self.field_file_colibration, 3, 3)

        self.win_mesurement.grid.addWidget(lbl_description, 5, 0)
        self.win_mesurement.grid.addWidget(qle_description, 4, 1, 4, 4)

        self.win_mesurement.grid.addWidget(field_img, 11, 0, 11, 4)

        self.win_mesurement.grid.addWidget(btn_rescan, 22, 0)
        self.win_mesurement.grid.addWidget(self.lbl_result, 22, 2)
        self.win_mesurement.grid.addWidget(btn_accept, 22, 3)

        # self.win_mesurement.show()

    def rescan(self):
        # os.chdir('process')
        data = self.opencv.image_processing()
        # pprint.pprint(data)

        # self.fieldImg.setPixmap(QPixmap('test-2-2.png'))
        text = 'PSA=0.53-0.081 ng/ml @ 97% confidence'
        self.lbl_result.setText(text)

        # self.lblResult.adjustSize()

    def get_file(self):
        # fname = QFileDialog.getOpenFileName(self, 'Open file',
        #                                     'c:\\', "Image files (*.jpg *.gif)")
        fname = QFileDialog.getOpenFileName(self.win_mesurement, 'Open file',
                                            '/home/user', "Image files (*.xml)")
        # print(fname)
        if fname != ('', ''):
            fname = os.path.split(fname[0])[1]
            self.field_file_colibration.deleteLater()
            self.field_file_colibration = self.label(fname)
            self.win_mesurement.grid.addWidget(self.field_file_colibration, 3, 3)

    def found_files_colibration(self):
        searched_files = os.listdir('colibration')
        pattern = '.*(\d{2,4}[-|:|_]?){6}(\.xml)$'
        colibration_files = []
        for name_file in searched_files:
            results = re.match(pattern, name_file)
            if results != None: colibration_files.append(name_file)

        return colibration_files

    def save(self):
        date = 'Дата'
        lot_number = self.qle_lot_number.text()
        description = 'PSA Calibration Curve SQ201'
        organization = self.qle_organization.text()
        position = self.qle_position.text()
        full_name = self.qle_fullName.text()
        phone = self.qle_phone.text()
        measurementResult =  self.lbl_result.text()
        test_type = self.combo_test_type.currentText()

        html = '<h1>Отчет</h1>'
        html += '<p>Дата: {}</p>'.format(date)
        html += '<p>Номер партии теста: {}</p>'.format(lot_number)
        html += '<p>Тип теста: {}</p>'.format(test_type)
        html += '<p>Описание: {}</p>'.format(description)
        html += '<h1>Результаты измерения</h1>'
        html += '<p>{}<p/>'.format(measurementResult)
        html += '<h1>Организация и оператор</h1>'
        html += '<p>Организация: {}</p>'.format(organization)
        html += '<p>Оператор: {}, {}</p>'.format(full_name, position)
        html += '<p>Телефон: {}</p>'.format(phone)
        html += '<h1>Данные калибровки</h1>'
        html += '<p>Серия: {}, срок годности: {}</p>'.format('F12181', 'Дата')
        html += '<p>Файл: {}, надежность: {}</p>'.format('Файл', '92.6%')
        html += '<p>Оператор: {}, {}</p>'.format('ФИО', 'должность')
        html += '<p>Телефон: {}</p>'.format('9999999999')
        pdf = pydf.generate_pdf(html, encoding='utf-8')
        os.chdir('process')
        with open('protocol_result.pdf', 'wb') as f:
            f.write(pdf)
        os.chdir('../')


        self.win_mesurement.deleteLater()