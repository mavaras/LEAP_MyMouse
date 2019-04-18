# -*- coding: utf-8 -*-

# ===============GUI CLASSES===============
# == Canvas
# == MainWindow
# == Cv_frames
# == leap_controller frames + leap_controller connected (signals)


# basic modules imports
import time
import sys
import numpy as np
import os

# aux modules imports
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
from PIL import Image
# import matplotlib.pyplot as plt  # conflict with sphinx

from scipy.misc import imresize
from sklearn import datasets
from sklearn import svm

# self package imports
from gvariables import *
import gvariables

from controllers.win32_functions import *
from controllers.key_handle import *
from controllers.aux_functions import *
from models.PCRecognizer import PCRecognizer
from models.points import Point, Point_cloud
from views.gui_qtdesigner import *
from views.canvas import Widget_canvas
from views.cv_frame import Cv_Frame


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    # last and new points for proper drawing (esto no se que mierda es)
    lp = Point(0, 0, -1)
    np = Point(0, 0, -1)
    n_of_fingers = 1

    """ this array stores all combo_boxes with its options with its associated gesture | gifs
    this in an array of dictionaries, each one containing each combo box index + gest. name
    dict key -> combobox index ; dict value -> conf. file string"""
    cb_action_gesture = {}

    # flag
    opened = False

    gvariables = None

    # alternating between pd an NN recognition systems
    canvas_algorithm = "pd"

    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowOpacity(0)
        self.opened = True
        self.systray = QSystemTrayIcon(QIcon("res/icon.ico"), self)
        self.set_notification_area()

        self.cvF = Cv_Frame(self)
        self.widget_canvas = None

        self.setupUi(self)

    def initUI(self):
        """ widget initialization, positioning, linking etc.
        fills cb_action_gesture array
        """

        print("initUI")

        # TAB1 - CANVAS setup
        self.widget_canvas = Widget_canvas(self.tab_canvas)  # linking widget_canvas to tab1
        self.widget_canvas.move(20, 20)
        self.widget_canvas.resize(canvas_width, canvas_height)

        canvas_algorithm_group = QtGui.QButtonGroup(self)
        self.radioButton_pd.toggled.connect(lambda: self.recognition_algorithm_ch("pd"))
        self.radioButton_NN.toggled.connect(lambda: self.recognition_algorithm_ch("NN"))
        canvas_algorithm_group.addButton(self.radioButton_pd)
        canvas_algorithm_group.addButton(self.radioButton_NN)

        # TAB2 - CONFIGURATION TAB
        self.button_save_conf.clicked.connect(self.save_conf)

        # text edits setup (not used)
        self.button_load_text.clicked.connect(self.load_text_B)
        self.text_edit.setReadOnly(True)
        self.text_edit_2.setReadOnly(True)
        self.combo_box.currentIndexChanged["int"].connect(self.combo_box_nfingers_selection_changed)

        # __label_leap_status default value
        self.change_leap_status(False)
        gvariables.listener.status.sgn_leap_connected.connect(self.change_leap_status)

        # __cv_frame representation
        gvariables.listener.status.sgn_cv_frame_XY.connect(self.cvF.set_frame_XY)
        gvariables.listener.status.sgn_cv_frame_XZ.connect(self.cvF.set_frame_XZ)

        # __Action-gesture COMBOBOXES
        # TODO: set all gestures the same as ComboBoxes and handle into leap_controller
        self.combo_box_mm.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_mm"))

        self.combo_box_click.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_click"))
        self.cb_action_gesture[self.combo_box_click] = {0: "click_planem",
                                                        1: "click_deepm",
                                                        2: "click_f2down",
                                                        3: "click_f1down",
                                                        4: "click_f0down"}

        self.combo_box_rclick.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_rclick"))
        self.cb_action_gesture[self.combo_box_rclick] = {0: "rclick_f2down",
                                                         1: "f1_f2_front",
                                                         2: "rclick_f1down"}

        self.combo_box_minimizew.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_minimizew"))
        self.cb_action_gesture[self.combo_box_minimizew] = {0: "V",
                                                            1: "T"}

        self.combo_box_closew.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_closew"))
        self.cb_action_gesture[self.combo_box_closew] = {0: "T",
                                                         1: "V"}

        self.combo_box_changew.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_changew"))
        self.cb_action_gesture[self.combo_box_changew] = {0: "90_and_swipe"}

        self.combo_box_vscroll.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_vscroll"))
        self.cb_action_gesture[self.combo_box_vscroll] = {0: "5_fingers_UD",
                                                          1: "5_fingers_LR",
                                                          2: "4_fingers_UD",
                                                          3: "3_fingers_UD"}

        self.combo_box_hscroll.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_hscroll"))
        self.cb_action_gesture[self.combo_box_hscroll] = {0: "default"}

        self.combo_box_grabb.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_grabb"))
        self.cb_action_gesture[self.combo_box_grabb] = {0: "f1_f2"}

        self.combo_box_showdesktop.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_showdesktop"))
        self.cb_action_gesture[self.combo_box_showdesktop] = {0: "D",
                                                              1: "T",
                                                              2: "V"}

        self.combo_box_openfexplorer.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_openfexplorer"))
        self.cb_action_gesture[self.combo_box_openfexplorer] = {0: "Z",
                                                                1: "D",
                                                                2: "X",
                                                                3: "V"}

        self.combo_box_copy.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_copy"))
        self.cb_action_gesture[self.combo_box_copy] = {0: "C",
                                                       1: "D",
                                                       2: "T",
                                                       3: "V"}

        self.combo_box_paste.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_paste"))
        self.cb_action_gesture[self.combo_box_paste] = {0: "V",
                                                        1: "T",
                                                        2: "C",
                                                        3: "D"}

        self.combo_box_cut.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_cut"))
        self.cb_action_gesture[self.combo_box_cut] = {0: "X",
                                                      1: "D",
                                                      2: "C",
                                                      3: "V"}

        # __help buttons
        self.set_gesture_gif("res/gifs/no_gesture.gif")
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())

        help_img = "res/eye.png"
        # we pass view_gesture() method help button associated combo box
        self.button_help_click.clicked.connect(lambda: self.view_gesture(self.combo_box_click))
        self.button_help_click.setIcon(QIcon(help_img))
        self.button_help_click.setIconSize(QSize(20, 20))
        self.button_help_click.setMask(QtGui.QRegion(self.button_help_click.rect(),
                                                     QtGui.QRegion.Ellipse))
        self.button_help_rclick.clicked.connect(lambda: self.view_gesture(self.combo_box_rclick))
        self.button_help_rclick.setIcon(QIcon(help_img))
        self.button_help_rclick.setIconSize(QSize(20, 20))
        self.button_help_rclick.setMask(QtGui.QRegion(self.button_help_rclick.rect(),
                                                      QtGui.QRegion.Ellipse))
        self.button_help_grabb.clicked.connect(lambda: self.view_gesture(self.combo_box_grabb))
        self.button_help_grabb.setIcon(QIcon(help_img))
        self.button_help_grabb.setIconSize(QSize(20, 20))
        self.button_help_grabb.setMask(QtGui.QRegion(self.button_help_grabb.rect(),
                                                     QtGui.QRegion.Ellipse))
        self.button_help_vscroll.clicked.connect(lambda: self.view_gesture(self.combo_box_vscroll))
        self.button_help_vscroll.setIcon(QIcon(help_img))
        self.button_help_vscroll.setIconSize(QSize(20, 20))
        self.button_help_vscroll.setMask(QtGui.QRegion(self.button_help_vscroll.rect(),
                                                       QtGui.QRegion.Ellipse))

        # TAB3
        """self.combo_box_gestures.currentIndexChanged["int"].connect(self.combo_box_gestures_selection_changed)
        self.set_gesture_gif("gifs/click_plane.gif")
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())"""

        # MENUBAR
        self.menubar_file_loadconf.triggered.connect(self.load_conf_file)
        self.menubar_file_saveconf.triggered.connect(self.save_conf)

    def set_notification_area(self):
        """ this function sets notification area menu"""

        self.systray.show()
        self.systray.showMessage("PCRecognizer",
                                 "App working",
                                 QSystemTrayIcon.Warning)
        # right click options
        self.systray_menu = QMenu(self)
        self.opt_startcontrol = self.systray_menu.addAction("Open/Close").triggered.connect(self.show_gui)  # open gui
        self.opt_startcontrol = self.systray_menu.addAction("Start Control").triggered.connect(self.start_stop_control)
        self.opt_stopcontrol = self.systray_menu.addAction("Stop Control").triggered.connect(self.start_stop_control)
        self.opt_exit = self.systray_menu.addAction("Exit").triggered.connect(self.exit_app)
        self.systray.setContextMenu(self.systray_menu)

    # this two functions are about loading text from text_edit and converting it to points array (not used)
    def to_point(self, text):
        parts = text.split(",")
        return int(float(parts[0][1:])), int(float(parts[1][:-1]))

    def load_text_B(self):
        text = str(self.text_edit.toPlainText())
        arr = text.split("\n")

        loaded_points = []  # containing new read points
        for c in range(2, len(arr) - 1):
            x, y = self.to_point(arr[c])
            loaded_points.append(Point(x, y, -1))

        pc = Point_cloud("loaded_points", loaded_points);
        self.widget_canvas.path = QPainterPath()  # clear canvas
        self.update()
        pc.draw_on_canvas()  # drawing loaded stroke
        global points
        points = loaded_points  # allowing "F"

    def save_conf(self):
        """ save Configuration object content to file"""

        print("save_conf()")
        fname = QFileDialog.getSaveFileName(self,
                                            "Save Configuration",
                                            "E:\\Documentos\\Estudio\\programming\\Python\\leap\\LEAP_proyect",
                                            "(*.txt)")
        if fname:
            f = open(fname, "w+")

            configuration = gvariables.configuration
            configuration.file_name = str(QFileInfo(fname).fileName())
            configuration.file_path = str(QFileInfo(fname).path())
            configuration.file_date = time.ctime(os.path.getctime(fname))

            f.write(configuration.file_name + "\n" + configuration.file_path + "\n" + configuration.file_date + "\n\n")
            f.write(configuration.basic.get_conf())
            f.write("\n")
            f.write(configuration.extra.get_conf())
            f.close()
        else:
            print("error save_conf()")

    def load_conf_file(self):
        """ loads configuration file into Configuration object"""

        print("load_conf_file()")
        fname = QFileDialog.getOpenFileName(self,
                                            "Save Configuration",
                                            "E:\\Documentos\\Estudio\\programming\\Python\\leap\\LEAP_proyect",
                                            "(*.txt)")
        if fname:
            f = open(fname, "r")
            gvariables.configuration.load_conf(f)

            f.close()

        self.label_conf_file.setText(str(fname))
        self.load_conf()

    def load_conf(self):
        """ loads given configuration object into SYSTEM
        updates comboboxes and GUI elements
        using cb_action_gesture array
        """

        self.combo_box_mm.setCurrentIndex(int(gvariables.configuration.basic.mm))

        self.combo_box_click.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_click], gvariables.configuration.basic.lclick)
        )

        self.combo_box_rclick.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_rclick], gvariables.configuration.basic.rclick)
        )

        self.combo_box_minimizew.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_minimizew], gvariables.configuration.basic.minimizew)
        )

        self.combo_box_closew.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_closew], gvariables.configuration.basic.closew)
        )

        self.combo_box_changew.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_changew], gvariables.configuration.basic.changew)
        )

        self.combo_box_vscroll.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_vscroll], gvariables.configuration.basic.vscroll)
        )

        self.combo_box_hscroll.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_hscroll], gvariables.configuration.basic.hscroll)
        )

    # Leap status label
    @pyqtSlot(bool)
    def change_leap_status(self, conn):
        """ handles Leap label status on the down bar
        :param conn: true if connected, false if not
        """
        if conn:
            self.label_leap_status.setText("CONNECTED")
            self.label_leap_status.setStyleSheet("QLabel {color: green;}")
        else:
            self.label_leap_status.setText("DISCONNECTED")
            self.label_leap_status.setStyleSheet("QLabel {color: red;}")

    def keyPressEvent(self, event):
        """ this is a collection of key events binded to GUI
        :param event: pressed key
        """

        global points
        if event.key() == QtCore.Qt.Key_Q:
            self.exit_app()

        elif event.key() == QtCore.Qt.Key_W:  # app interaction example/test
            """handle = win32gui.FindWindow(None, r"Reproductor multimedia VLC")
            # win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)
            win32gui.CloseWindow(handle)"""

            print("w")

        elif event.key() == QtCore.Qt.Key_S:
            gvariables.listener.mouse.active = True if not gvariables.listener.mouse.active else False

        elif event.key() == QtCore.Qt.Key_Y:
            """print("Y pressed")
            keyboard = Controller()
            keyboard.press(Key.cmd)
            keyboard.press("d")
            keyboard.release("d")
            keyboard.release(Key.cmd)"""

        elif event.key() == QtCore.Qt.Key_F:  # start stroke recognition
            if self.n_of_fingers == 1:
                pc = Point_cloud("f1", self.widget_canvas.points, Point(W/4, H/4 + 50, -1))
                # pc.draw_on_canvas()    normalized pc

                result = recognize_stroke(self.widget_canvas.points)
                gesture_match(result.name)

                str_accum = "Last/Current gesture points array\n\n"
                for c in range(0, len(points)):
                    str_accum += "(" + str(points[c].x) + "," + str(points[c].y) + ")"
                    if c != len(points) - 1:
                        str_accum += "\n"

                print_score(result)
                self.text_edit.setText(str_accum)

            elif self.n_of_fingers == -1:
                results = []
                for c in range(0, 5):
                    results.append(recognize_stroke(gvariables.listener.gesture[c]))
                    gesture_match(results[len(results) - 1].name)

                results_names = [res.name for res in results]
                print(results_names)
                if len(set(results_names)) <= 1:
                    print_score(results[1])
                else:
                    print("inconsistent matches of each finger")

            # resetting values, clearing arrays
            gvariables.stroke_id = 0
            points = []
            gvariables.listener.clear_variables()

        elif event.key() == QtCore.Qt.Key_C:  # clear canvas
            print("clear")
            self.widget_canvas.clear()
            self.label_score.setText("")

        elif event.key() == QtCore.Qt.Key_G and sys.argv[1] != "-thread":
            # global points
            if self.n_of_fingers == 1:  # recordin only 1 finger(indice)
                print("1 finger recording mode")
                if gvariables.listener.capture_frame:  # 2nd "G" press
                    print("record captured")
                    gvariables.listener.capture_frame = False

                    if self.canvas_algorithm == "NN":
                        # neural network things
                        img_dim = 28
                        matrix = np.zeros((img_dim, img_dim, 3), dtype=np.uint8)
                        white = [255, 255, 255]
                        # leap_gesture_points = gvariables.listener.gesture[1]
                        max_leap_y = max(g.y for g in gvariables.listener.gesture[1])
                        max_leap_x = max((g.x + 200) for g in gvariables.listener.gesture[1])

                        """img_dim = int(max_leap_y/11)
                        matrix = np.zeros((img_dim, img_dim, 3), dtype=np.uint8)"""
                        for c in range(len(gvariables.listener.gesture[1])):
                            leap_x = gvariables.listener.gesture[1][c].x + 140
                            leap_y = max_leap_y + 40 - gvariables.listener.gesture[1][c].y
                            print(str(leap_x) + ", " + str(leap_y))
                            print(str(leap_x * img_dim / max_leap_x) + "; " + str(leap_y * img_dim / max_leap_y))
                            print("")
                            matrix_x = int(leap_x * img_dim / max_leap_x)
                            matrix_x = 27 if matrix_x == 28 else matrix_x
                            matrix_y = int(leap_y * img_dim / max_leap_y)
                            matrix_y = 27 if matrix_y == 28 else matrix_y
                            matrix[matrix_y][matrix_x] = white

                        print("max X: " + str(max_leap_x))
                        print("max Y: " + str(max_leap_y))
                        img = self.matrix_to_img(matrix)
                        self.neural_network(img)

                    else:
                        # p dollar algorithm (default)
                        leap_gesture_points = gvariables.listener.gesture[1]
                        pc = Point_cloud("f1", leap_gesture_points).draw_on_canvas()
                        # img = self.matrix_to_img(gvariables.listener.gesture[1])

                        result = recognize_stroke(leap_gesture_points)
                        gesture_match(result.name)

                        str_accum = "Last/Current gesture points array\n\n"
                        for c in range(0, len(points)):
                            str_accum += "(" + str(points[c].x) + "," + str(points[c].y) + ")"
                            if c != len(points) - 1:
                                str_accum += "\n"

                        print_score(result)
                        self.text_edit.setText(str_accum)

                        # getting finger_1 points
                        points = gvariables.listener.gesture[1]  # this allows "F" to work with mouse and hand stroke

                else:  # 1st "G" press
                    print("recording")
                    self.label_count.setText("4")  # countdown after getting gesture
                    # this is like a thread with no wait
                    QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(self.label_count))

            elif self.n_of_fingers == -1:  # recording ALL fingers
                print("all fingers recording mode")
                aux = -100
                if gvariables.listener.capture_frame:
                    print("record captured")
                    gvariables.listener.capture_frame = False
                    for c in range(0, 5):
                        pc = Point_cloud("f" + str(c), gvariables.listener.gesture[c], Point(W / 4 + aux, H / 4, -1))
                        pc.draw_on_canvas()
                        aux += 50

                    points = gvariables.listener.gesture[1]  # just for testing

                else:  # 1st "G" press
                    print("recording")
                    self.label_count.setText("4")  # countdown after getting gesture
                    # this is like a thread with no wait
                    QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(self.label_count))

    def show_gui(self):
        """ this handles notification area option 'Open/Close'
        hide or shows MainWindow
        """
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def matrix_to_img(self, matrix):
        """ this function is related to neural network
        convert provided np matrix to .png image
        :param matrix: converts given matrix to an 28x28 image (NN)
        """

        img = Image.fromarray(matrix, "RGB")
        # img.thumbnail((28, 28), Image.ANTIALIAS)  # resizing to 28x28
        img.save("image_28x28.png")
        img.show()

        # dilate image
        img = cv2.imread("image_28x28.png", cv2.IMREAD_GRAYSCALE)
        img = cv2.dilate(img, np.ones((3, 3), np.uint8), iterations=2)
        # img = cv2.erode(img, np.ones((3, 3), np.uint8), iterations=1)

        return img

    def neural_network(self, img):
        """ passes provided image through neural network"""

        # setting + normalizing image
        cv2.imshow("image", cv2.resize(img, (200, 200)))
        img = np.delete(img, np.where(~img.any(axis=1))[0], axis=0)
        img = np.delete(img, np.where(~img.any(axis=0))[0], axis=1)
        img = cv2.resize(img, (8, 8))
        minValueInImage = np.min(img)
        maxValueInImage = np.max(img)
        img = np.floor(np.divide((img - minValueInImage).astype(np.float),
                                 (maxValueInImage - minValueInImage).astype(np.float)) * 16)
        print(img)

        # loading digit database
        digits = datasets.load_digits()
        n_samples = len(digits.images)
        data = digits.images.reshape((n_samples, -1))

        # setting classifier
        clf = svm.SVC(gamma=0.0001, C=100)
        clf.fit(data[:n_samples], digits.target[:n_samples])

        # predict
        predicted = clf.predict(img.reshape((1, img.shape[0] * img.shape[1])))

        # display results
        """for c in range(8):
            for j in range(8):
                if img[c][j] > 0:
                    img[c][j] = 16"""
        print("prediction: " + str(predicted))
        plt.imshow(img, cmap=plt.cm.gray_r, interpolation="nearest")
        plt.title("result: " + str(predicted))
        plt.show()

    def recognition_algorithm_ch(self, what):
        """
        handles check box selecting recognition algorithm
        :param what: 'pd' or 'NN'
        """
        print("canvas algorithm changed to " + str(what))
        if what == "pd":
            self.canvas_algorithm = "pd"
        else:
            self.canvas_algorithm = "NN"

    def combo_box_nfingers_selection_changed(self):
        print("selection changed" + str(self.combo_box.currentIndex()))
        if self.combo_box.currentIndex() == 0:
            self.n_of_fingers = 1
        elif self.combo_box.currentIndex() == 1:
            self.n_of_fingers = -1

        self.setFocus()  # getting focus back on main_window

    def combo_box_actiongesture_changed(self, combo_box_name):
        """ collection of key events binded to GUI (configuration tab comboboxes)
        :param combo_box_name: changed combobox variable name"""

        if combo_box_name == "combo_box_click":
            print("lclick changed" + str(self.combo_box_click.currentIndex()))
            gvariables.configuration.basic.lclick = self.cb_action_gesture[self.combo_box_click] \
                .get(self.combo_box_click.currentIndex())

        elif combo_box_name == "combo_box_rclick":
            print("rclick changed")
            print(self.cb_action_gesture[self.combo_box_rclick] \
                  .get(self.combo_box_rclick.currentIndex()))
            gvariables.configuration.basic.rclick = self.cb_action_gesture[self.combo_box_rclick] \
                .get(self.combo_box_rclick.currentIndex())

        elif combo_box_name == "combo_box_mm":
            gvariables.configuration.basic.mm = self.combo_box_mm.currentIndex()

        elif combo_box_name == "combo_box_minimizew":
            gvariables.configuration.basic.minimizew = self.cb_action_gesture[self.combo_box_minimizew] \
                .get(self.combo_box_minimizew.currentIndex())

        elif combo_box_name == "combo_box_closew":
            gvariables.configuration.basic.closew = self.cb_action_gesture[self.combo_box_closew] \
                .get(self.combo_box_closew.currentIndex())

        elif combo_box_name == "combo_box_changew":
            gvariables.configuration.basic.changew = self.cb_action_gesture[self.combo_box_changew] \
                .get(self.combo_box_changew.currentIndex())

        elif combo_box_name == "combo_box_vscroll":
            gvariables.configuration.basic.vscroll = self.cb_action_gesture[self.combo_box_vscroll] \
                .get(self.combo_box_vscroll.currentIndex())

        elif combo_box_name == "combo_box_hscroll":
            gvariables.configuration.basic.hscroll = self.cb_action_gesture[self.combo_box_hscroll] \
                .get(self.combo_box_hscroll.currentIndex())

        elif combo_box_name == "combo_box_grabb":
            gvariables.configuration.basic.grabb = self.cb_action_gesture[self.combo_box_grabb] \
                .get(self.combo_box_grabb.currentIndex())

        self.setFocus()

    # (not used)
    def combo_box_gestures_selection_changed(self):  # not used
        print("selection changed" + str(self.combo_box_gestures.currentIndex()))
        if self.combo_box_gestures.currentIndex() == 0:
            self.set_gesture_gif("res/gifs/click_plane.gif")
        elif self.combo_box_gestures.currentIndex() == 1:
            self.set_gesture_gif("res/gifs/grabb_plane.gif")
        elif self.combo_box_gestures.currentIndex() == 2:
            self.set_gesture_gif("res/gifs/scroll.gif")

        self.setFocus()

    def view_gesture(self, combo_box):
        """ loads gesture associated gif
        :params combo_box: gif button associated combobox variable name
        """

        print("view gesture: " + str(combo_box.currentIndex()))
        print(self.cb_action_gesture.get(combo_box).get(combo_box.currentIndex()))

        self.set_gesture_gif(
            "res/gifs/" + str(self.cb_action_gesture.get(combo_box).get(combo_box.currentIndex())) + ".gif")
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())

    def start_stop_control(self):
        """ this handles the click event to "Start Control" or "Stop Control" into notification
        area icon
        """

        print("notification area Start/Stop Control")

        if not gvariables.listener.status.leap_connected:
            self.show_popup("Problem Detected",
                            "Leap Motion error",
                            "Leap Motion device is not connected")
        else:
            if gvariables.configuration.check():
                gvariables.listener.mouse.active = True if not gvariables.listener.mouse.active else False

            else:
                self.show_popup("Problem Detected",
                                "Configuration error",
                                "You have same gesture assigned to multiple actions in your configuration")

    """def set_label_leap_status(self, img):
        Leap status label CONNECTED or DISCONNECTED

        img, _, _ = load_image(img)
        self.label_leap_status.setPixmap(QPixmap.fromImage(img))"""

    def set_gesture_gif(self, gif):
        """ loads given gif into gif label
        :param gif: .gif file
        """
        giff = QtGui.QMovie(gif)
        self.label_gesture_gif.setMovie(giff)
        giff.start()

    def updateLabel(self, label):
        """ this function handles countdown label"""

        # change the following line to retrieve the new voltage from the device
        t = int(label.text()) - 1
        if t == 0:
            label.setText("")
            while (gvariables.listener.hand_vel < 270 or gvariables.listener.fingers_vel[4] < 100):
                pass

            gvariables.listener.capture_frame = True
            return

        label.setText(str(t))
        QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(label))

    def show_popup(self, title, text, inftext):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(text)
        msg.setInformativeText(inftext)
        msg.setWindowTitle(title)
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def exit_app(self):
        """ ends app execution and closes all windows"""

        print("exiting...")
        self.close()
        sys.exit()
        self.opened = False
