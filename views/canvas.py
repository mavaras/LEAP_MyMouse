# -*- coding: utf-8 -*-

# ===============CANVAS===============
# == canvas test window, for debugging and testing purposes
# == $d and NN
# == canvas widget


import numpy as np

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from views.gui_qtdesigner import *

import cv2
from PIL import Image
import matplotlib.pyplot as plt  # conflict with sphinx
from sklearn import datasets
from sklearn.externals import joblib

# from models.PCRecognizer import *
from models.points import Point
from controllers.aux_functions import *

stroke_id = -1


class Canvas(QDialog):
    """ this class represents the canvas window where canvas widget is displayed"""

    def __init__(self, parent):
        super(Canvas, self).__init__(parent)

        self.parent = parent

        self.setWindowTitle("Canvas")
        self.setWindowIcon(QtGui.QIcon("res/icons/leapmymouse.png"))

        self.resize(400, 600)
        self.setFixedSize(self.size())

        self.n_of_fingers = 1
        self.canvas_algorithm = "pd"

        self.widget_canvas = Widget_canvas(self, 400, 400)
        self.widget_canvas.move(20, 20)

        self.label_opts = QLabel()
        self.label_opts.setText("V D T X W Z L")

        layout = QVBoxLayout()
        layout.addWidget(self.widget_canvas, 85)

        self.label_score = QLabel()
        self.label_score.setText("")
        layout.addWidget(self.label_score)

        vbox1 = QHBoxLayout()
        self.cb_algorithm = QComboBox()
        self.cb_algorithm.addItem("p$ Recognizer      ")
        self.cb_algorithm.addItem("NN - Neural Network")
        self.cb_algorithm.currentIndexChanged["int"].connect(self.recognition_algorithm_ch)
        vbox1.addWidget(self.cb_algorithm, 30)
        vbox1.addStretch(13)
        vbox1.addWidget(self.label_opts, 30)
        layout.addLayout(vbox1, 8)
        layout.addStretch(2)

        stylesheet = """image: none;
                     border-color: rgb(77,77,77);
                     border-style: solid;
                     border-width: 1px;
                     border-radius: 6px;
                     color: color_label;"""

        vbox2 = QHBoxLayout()
        button_clear = QPushButton("clear")
        button_clear.setStyleSheet(stylesheet)
        button_clear.clicked.connect(self.clear)

        button_recognize = QPushButton("recognize")
        button_recognize.setStyleSheet(stylesheet)
        button_recognize.clicked.connect(self.recognize)

        vbox2.addWidget(button_clear, 20)
        vbox2.addWidget(button_recognize, 20)
        layout.addLayout(vbox2, 7)

        self.setLayout(layout)

    def recognition_algorithm_ch(self):
        """ handles combobox recognition algorithm changes"""

        print("canvas algorithm changed")
        if self.cb_algorithm.currentIndex() == 0:
            self.canvas_algorithm = "pd"
            self.label_opts.setText("V D T X W Z L")

        else:
            self.canvas_algorithm = "NN"
            self.label_opts.setText("1 2 3 4 5 6 7 8 9")

        self.widget_canvas.clear()
        self.label_score.setText("")

    def clear(self):
        """ removes all strokes from canvas"""

        print("clear")
        self.widget_canvas.clear()
        self.label_score.setText("")
        self.recognition_algorithm_ch()

    def recognize(self):
        """ recognizes canvas's stroke"""

        if self.canvas_algorithm == "pd":
            # we are using p$ recognizer
            points = self.widget_canvas.points
            result = recognize_stroke(self.widget_canvas.points)

            str_accum = "Last/Current gesture points array\n\n"
            for c in range(0, len(points)):
                str_accum += "(" + str(points[c].x) + "," + str(points[c].y) + ")"
                if c != len(points) - 1:
                    str_accum += "\n"

            print_score(result, self.parent)

        else:
            # we are using NN
            leap_gesture_points = self.widget_canvas.points

            # undoing convert_to from leap_controller to get min and max
            min_x = min(g.x for g in leap_gesture_points) - 20
            min_y = min(g.y for g in leap_gesture_points)
            max_y = max(g.y for g in leap_gesture_points)
            max_x = max(g.x for g in leap_gesture_points)
            matrix = np.zeros((int(max_y - min_y) + 40+min_y,
                               int(max_x - min_x) + 40+min_x, 3),
                              dtype=np.uint8)
            white = [255, 255, 255]
            for c in range(len(leap_gesture_points)):
                matrix[int(leap_gesture_points[c].y)][int(leap_gesture_points[c].x)] = white

            img = self.matrix_to_img(matrix)
            self.neural_network(img)

        self.parent.listener.clear_variables()

    def matrix_to_img(self, matrix):
        img = Image.fromarray(matrix, "RGB")
        img.save("res/image_28x28.png")

        # dilate image
        img = cv2.dilate(cv2.imread("res/image_28x28.png", cv2.IMREAD_GRAYSCALE),
                         np.ones((5, 5), np.uint8), iterations=6)
        cv2.imshow("28x28 saved & dilated image", img)

        return img

    def neural_network(self, img):
        # setting + normalizing image
        img = cv2.resize(img, (28, 28))
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

        # loading digit database
        """digits = datasets.load_digits()
        n_samples = len(digits.images)
        data = digits.images.reshape((n_samples, -1))"""

        # predict EMNIST
        self.parent._print("Loading MLP model from file res/mlp_model.pkl")
        clf = joblib.load("res/mlp_model.pkl").best_estimator_
        predicted = clf.predict(img.reshape((1, img.shape[0] * img.shape[1])))

        # display results
        self.parent._print("prediction: " + str(predicted))
        plt.imshow(img, cmap=plt.cm.gray_r, interpolation="nearest")
        plt.title("result: " + str(predicted))
        plt.show()


class Widget_canvas(QWidget):
    """ this class refers just to the canvas widget where user draw"""

    def __init__(self, parent, w, h):
        super(Widget_canvas, self).__init__(parent)

        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.points = []
        self.lp = Point(0, 0, -1)
        self.np = Point(0, 0, -1)

        self.path_points_0 = QPainterPath()
        self.path_points_1 = QPainterPath()
        self.path_points_2 = QPainterPath()
        self.path_points_3 = QPainterPath()
        self.path_points_4 = QPainterPath()

        self.canvas = None
        self.pen_color = Qt.white

        self.canvas_width = w
        self.canvas_height = h
        self.resize(self.canvas_width, self.canvas_height)

    def clear(self):
        """ clears the canvas, resetting all QPainterPaths"""

        aux = QPainterPath()
        self.path_points_0 = aux
        aux = QPainterPath()
        self.path_points_1 = aux
        aux = QPainterPath()
        self.path_points_2 = aux
        aux = QPainterPath()
        self.path_points_3 = aux
        aux = QPainterPath()
        self.path_points_4 = aux

        self.points = []
        self.lp = Point(0, 0, -1)
        self.np = Point(0, 0, -1)

        self.update()

    def paintEvent(self, event):
        """ QWidget main paint event. Everything is drawn here"""

        canvas = QtGui.QPainter(self)
        pen = QPen()

        # drawing grid
        pen.setWidth(1.4)
        pen.setColor(QColor(77, 77, 77))
        canvas.setPen(pen)
        interval = 20
        for c in range(interval, self.canvas_width, interval):
            for j in range(interval, self.canvas_height, interval):
                canvas.drawLine(c, 0, c, self.canvas_height)
                canvas.drawLine(0, j, self.canvas_width, j)

        # finger 0 path
        pen.setWidth(2.4)
        pen.setColor(Qt.red)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_0)

        # finger 1 path
        pen.setColor(Qt.white)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_1)

        # finger 2 path
        pen.setColor(Qt.blue)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_2)

        # finger 3 path
        pen.setColor(Qt.green)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_3)

        # finger 4 path
        pen.setColor(Qt.yellow)
        canvas.setPen(pen)
        canvas.drawPath(self.path_points_4)

    def mousePressEvent(self, event):
        """ captures a mouse click on the canvas"""

        x = event.x()
        y = event.y()
        print("start point: (" + str(x) + "," + str(y) + ")")

        self.path_points_1.addEllipse(QtCore.QRectF(x, y, 16, 16))
        global stroke_id  # , points
        stroke_id += 1
        self.points.append(Point(x, y, stroke_id))
        self.lp.x, self.lp.y = x, y

    def mouseMoveEvent(self, event):
        """ captures a cursor movement while mouse is pressed on the canvas"""

        x = event.x()
        y = event.y()
        self.np = Point(x, y, -1)
        if distance(self.lp, self.np) > 5:
            self.path_points_1.addEllipse(QtCore.QRectF(x, y, 8, 8))
            global stroke_id
            self.points.append(Point(x, y, stroke_id))
            self.lp.x, self.lp.y = x, y
            self.update()

    def mouseReleaseEvent(self, event):
        """ captures a mouse click release on the canvas"""

        print("end point: (" + str(event.x()) + "," + str(event.y()) + ")")
