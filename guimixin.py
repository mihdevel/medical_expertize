import os
import numpy
import pprint
import cv2 as cv

# from PyQt5.QtGui import QIcon, QPixmap


class GuiMixin:
    """docstring for GuiMixin"""

    def __init__(self, filename):
        self.filename = filename
        self.name_file_img_with_counturs = filename.split('.')[0] + '_with_counturs.' + filename.split('.')[1]
        self.data = []
        # self.get_picture()
        self._find_contours()

    def get_picture(self):
        capture = cv.VideoCapture(1)
        ret, frame = capture.read()
        os.chdir('process')
        cv.imwrite(self.filename, frame)
        os.chdir('../')

    def _find_contours(self, value=127):
        img = cv.imread(self.filename)
        self.img_croped = img
        # self.img_croped = img[290:650, 370:1100]
        imgray = cv.cvtColor(self.img_croped, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, value, 255, 0)
        imginvert = cv.bitwise_not(thresh)
        contours = cv.findContours(imginvert, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        img_with_counturs = cv.drawContours(self.img_croped, contours[1], -1, (0,255,0), 2)
        cv.imwrite(self.name_file_img_with_counturs, img_with_counturs)
        return contours

    def image_processing(self, reload_foto=None):
        # if reload_foto: os.chdir('process')
        #
        # for x in range(100, 227, 27):
        #     contours = self._find_contours(x)
        #
        #     data_stripes = []
        #     Y = []
        #     img_width = self.img_croped.shape[1]
        #     stripes = {
        #         'C': None,
        #         'N': None,
        #         'T': None,
        #     }
        #
        #     for contour in contours:
        #         if len(contour) < 400:
        #             continue
        #         # pprint.pprint(contour[1][0][0][0])
        #         # print(contour[0][0][0][0])
        #
        #
        #         Y.append(contour[0][0])
        #         y_mean = numpy.mean(Y)
        #         y_persent = int(y_mean / img_width * 100)
        #         data_stripes.append({'contour_stripe': contour, 'y_mean': y_mean, 'y_persent': y_persent})
        #
        #         for stripe in data_stripes:
        #             y_persent = stripe['y_persent']
        #
        #             if y_persent < 40 and stripes['C']: stripes['C'] = stripe
        #             elif 40 < y_persent < 60 and stripes['N']: stripes['N'] = stripe
        #             elif y_persent > 60 and stripes['T']: stripes['T'] = stripe
        #
        #
        #     self.data.append(stripes)
        a = [
            {
                'C': {'contour_stripe': 'contour', 'y_mean': 'y_mean', 'y_persent': 'y_persent'},
                'N': None,
                'T': {'contour_stripe': 'contour', 'y_mean': 'y_mean', 'y_persent': 'y_persent'},
            },
            {
                'C': None,
                'N': None,
                'T': {'contour_stripe': 'contour', 'y_mean': 'y_mean', 'y_persent': 'y_persent'},
            }
        ]

        result = {
                'C': None,
                'N': None,
                'T': None,
            }
        for mesure in a:
            if mesure['C']: result['C'] = mesure['C']
            if mesure['N']: result['N'] = mesure['N']
            if mesure['T']: result['T'] = mesure['T']


        pprint.pprint(result)


        # new_name_file = 'img-' + str(len(data_stripes) + 1) + '.png'
        # os.rename(self.name_file_img_with_counturs, new_name_file)
        # self.name_file_img_with_counturs = new_name_file

        if reload_foto: os.chdir('../')
        return self.data

        #         founded_contours_stripes.append(contour)
        # for contour_stripes in founded_contours_stripes:
        #     Y = []
        #     for contour_stripe in contour_stripes:
        #         print(contour_stripe)
        #         Y.append(contour_stripe[0][0])
        #
        #         y_mean = numpy.mean(Y)
        #
        #         y_persent = int(y_mean / img_width * 100)
        #         # print "{}%".format(y_persent)
        #
        #     data_stripes.append({'contour_stripe': contour_stripes, 'y_mean': y_mean, 'y_persent': y_persent})

        # for stripe in data_stripes:
        #     y_persent = stripe['y_persent']
        #
        #     if y_persent < 40 and stripes['C'] == 'false':
        #         stripes['C'] = stripe
        #
        #     elif 40 < y_persent < 60 and stripes['N'] == 'false':
        #         stripes['N'] = stripe
        #
        #     elif y_persent > 60 and stripes['T'] == 'false':
        #         stripes['T'] = stripe

    def calculate_result(self):
        # self.fieldImg.setPixmap(QPixmap('test-2-2.png'))
        text = 'PSA=0.53-0.081 ng/ml @ 97% confidence'
        self.lblResult.setText(text)
        # self.lblResult.adjustSize()


    # def add_table_column_value(self, row, column, value):
    #     self.table.setRowCount(row+1)
    #     self.table.setItem(row, column, QTableWidgetItem(value))


if __name__ == '__main__':
    class TestMixin(GuiMixin):
        def __init__(self):
            pass

    TestMixin()