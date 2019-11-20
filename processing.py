# import numpy as np
import numpy
import cv2 as cv


class GetPicture:
    def __init__(self, filename):
        capture = cv.VideoCapture(1)
        ret, frame = capture.read()
        cv.imwrite(filename, frame)

        # if capture.isOpened():
        # else:
        #     ret = False
        #     frame = cv.QueryFrame(capture)
        #     cv.SaveImage(filename, frame)


        # self.filename = filename
        # self.frame = frame



    # def get_filename(self):
    #     return self.filename

class ImgShow:
    """docstring for ImgShow"""

    def __init__(self, img, filename):
        # capture.release()
        title = filename
        cv.namedWindow(title, cv.WINDOW_NORMAL)
        cv.resizeWindow(title, 1000, 600)
        cv.imshow(title, img)
        k = cv.waitKey(0)

        if k == 27:  # wait for ESC key to exit
            cv.destroyAllWindows()
        elif k == ord('s'):  # wait for 's' key to save and exit
            cv.imwrite(filename, img)
            cv.destroyAllWindows()


class FindContours():
    """docstring for FindContours"""

    def __init__(self, filename):
        img = cv.imread(filename)

        # test-1.png
        # img_croped = img[290:650, 170:1000]

        # test-2-1.png
        # img_croped = img[290:650, 370:1100]

        # test-2-2.png
        img_croped = img[290:650, 370:1100]

        # test-3.png
        # img_croped = img[240:600, 200:1100]

        # hsv_min = np.array((2, 38, 65), np.uint8)
        # hsv_max = np.array((26, 238, 255), np.uint8)

        # hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # thresh = cv.inRange(hsv, hsv_min, hsv_max)
        # contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


        imgray = cv.cvtColor(img_croped, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 127, 255, 0)

        # thresh = cv.inRange(imgray, 127, 255)
        imginvert = cv.bitwise_not(thresh)

        contours = cv.findContours(imginvert, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        self.contours = contours
        self.width = img_croped.shape[1]

        # For python 2
        # img_with_counturs = cv.drawContours(img_croped, contours, -1, (0,255,0), 2, cv.LINE_AA, hierarchy, 1)
        img_with_counturs = cv.drawContours(img_croped, contours[1], -1, (0,255,0), 2)


        # for i in contours:
        #     for j in i:
        #         print j[0]
        #     print 'next list'
        # x, y, w, h = cv.boundingRect(contours[0])
        # cv.rectangle(img_with_counturs (x, y), (x + w, y + h), (0,255,0), 2)
        # print (x, y), (x + w, y + h)

        ImgShow(img_with_counturs, filename)


    def get_contours(self):
        return self.contours

    def get_width(self):
        return self.width


class ContoursProcess():
    """docstring for ContoursProcess"""

    def __init__(self, contours, img_width):
        found_contours_stripes = []
        self.data = []
        for contour in contours:
            if len(contour) > 100:
                # print len(contour)
                found_contours_stripes.append(contour)

        for contour_stripes in found_contours_stripes:
            Y = []
            for contour_stripe in contour_stripes:
                Y.append(contour_stripe[0][0])

                y_mean = numpy.mean(Y)

                y_persent = int(y_mean / img_width * 100)
                # print "{}%".format(y_persent)

            self.data.append({'contour_stripe': contour_stripes, 'y_mean': y_mean, 'y_persent': y_persent})
        # print data


    def identifiti(self):
        data = ''
        for y in self.data:
            y_persent = y['y_persent']
            if y_persent < 40:
                data = data + '1'
                # return '1'
            elif 40 < y_persent < 60:
                data = data + '2'
                # return '2'
            elif y_persent > 60:
                data = data + '3'
                # return '3'

        return data


results = (
    {'krov':
         {'yes': '123',
          'no': '1',
          'error': '2',
          }
     }
)


class Main:
    filename = 'test-2-2.png'
    #GetPicture(filename)
    fined_contours = FindContours(filename)
    contours = fined_contours.get_contours()
    img_width = fined_contours.get_width()

    process = ContoursProcess(contours, img_width)
    pologenie = process.identifiti()
    # print pologenie
    print(pologenie)

if __name__ == '__main__':
    Main()