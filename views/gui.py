# -*- coding: utf-8 -*-

# ===============GUI CLASSES===============
# == Canvas
# == MainWindow
# == Cv_frames
# == leap_controller frames + leap_controller connected (signals)


# basic modules imports
import sys
import numpy as np

# aux modules imports
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
from PIL import Image
import matplotlib.pyplot as plt  # conflict with sphinx

from sklearn import datasets
from sklearn.externals import joblib

# self package imports
from gvariables import gv
from _print import _print
from controllers.aux_functions import *
from models.points import Point, Point_cloud
from models.configuration_fromFile import ConfFromFile
from views.gui_qtdesigner import *
from views.canvas import Canvas
from views.settings import Settings
from views.cv_frame import Cv_Frame


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    """ this array stores all combo_boxes with its options with its associated gesture | gifs
    this in an array of dictionaries, each one containing each combo box index + gest. name
    dict key -> combobox index ; dict value -> conf. file string"""
    cb_action_gesture = {}

    # flag
    opened = False

    gv = None

    # changing between pd an NN recognition systems
    canvas_algorithm = "pd"

    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)

        self.opened = True
        self.systray = QSystemTrayIcon(QIcon("res/icons/leapmymouse.PNG"), self)
        self.set_notification_area()

        self.cvF = Cv_Frame(self)
        self.widget_canvas = None
        self.canvas = Canvas(self)
        self.settings = Settings(self)

        self.setupUi(self)

    def initUI(self):
        """ widget initialization, positioning, linking etc.
        fills cb_action_gesture array
        """

        self.setWindowIcon(QtGui.QIcon("res/icons/leapmymouse.png"))

        # launch on startup checkbox
        self.checkBox_startup.stateChanged.connect(lambda: self.launch_on_startup())

        # CONFIGURATION TAB

        # label_leap_status default value
        self.change_leap_status(gv.listener.status.leap_connected)
        gv.listener.status.sgn_leap_connected.connect(self.change_leap_status)

        # cv_frame representation
        gv.listener.status.sgn_cv_frame_XY.connect(self.cvF.set_frame_XY)
        gv.listener.status.sgn_cv_frame_XZ.connect(self.cvF.set_frame_XZ)

        # Action-gesture COMBOBOXES
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
        self.cb_action_gesture[self.combo_box_rclick] = {0: "rclick_f2down",
                                                         1: "f1_f2_front",
                                                         2: "rclick_f1down"}

        self.combo_box_minimizew.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_minimizew"))
        self.cb_action_gesture[self.combo_box_minimizew] = {0: "V",
                                                            1: "T",
                                                            2: "W",
                                                            3: "D",
                                                            4: "M"}
        self.combo_box_rclick.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_rclick"))

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
                                                              2: "V",
                                                              3: "Z",
                                                              4: "W"}

        self.combo_box_openfexplorer.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_openfexplorer"))
        self.cb_action_gesture[self.combo_box_openfexplorer] = {0: "X",
                                                                1: "Z",
                                                                2: "D",
                                                                3: "V",
                                                                4: "W"}

        self.combo_box_copy.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_copy"))
        self.cb_action_gesture[self.combo_box_copy] = {0: "C",
                                                       1: "D",
                                                       2: "T",
                                                       3: "V",
                                                       4: "W"}

        self.combo_box_paste.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_paste"))
        self.cb_action_gesture[self.combo_box_paste] = {0: "V",
                                                        1: "T",
                                                        2: "C",
                                                        3: "D",
                                                        4: "W"}

        self.combo_box_cut.currentIndexChanged["int"].connect(
            lambda: self.combo_box_actiongesture_changed("combo_box_cut"))
        self.cb_action_gesture[self.combo_box_cut] = {0: "W",
                                                      1: "X",
                                                      2: "D",
                                                      3: "C",
                                                      4: "V"}

        # help buttons
        self.set_gesture_gif("res/gifs/no_gesture.gif")
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())

        help_img = "res/icons/eye.png"
        # we pass view_gesture() method help button associated combo box
        self.button_help_click.clicked.connect(lambda: self.view_gesture(self.combo_box_click))
        self.button_help_rclick.clicked.connect(lambda: self.view_gesture(self.combo_box_rclick))
        self.button_help_grabb.clicked.connect(lambda: self.view_gesture(self.combo_box_grabb))
        self.button_help_vscroll.clicked.connect(lambda: self.view_gesture(self.combo_box_vscroll))
        self.button_setprofilename.clicked.connect(self.set_profile_name)
        self.lineEdit_profilename.setText("")

        self.button_stop.setChecked(True)
        self.button_stop.clicked.connect(lambda: self.start_stop_control())
        self.button_start.setChecked(False)
        self.button_start.clicked.connect(lambda: self.start_stop_control())

        # MENUBAR
        self.menubar_file_loadconf.triggered.connect(self.load_conf_file)
        self.menubar_file_saveconf.triggered.connect(self.save_conf)
        self.menubar_file_loaddefconf.triggered.connect(self.set_default_conf)
        self.menubar_help_debug.triggered.connect(self.debug_mode)
        self.menubar_help_settings.triggered.connect(self.show_settings)

    def set_notification_area(self):
        """ this function sets notification area menu"""

        self.systray.show()
        self.systray.showMessage("LEAP MyMouse",
                                 "App working",
                                 QSystemTrayIcon.NoIcon)
        # right click options
        self.systray_menu = QMenu(self)
        self.opt_startcontrol = self.systray_menu.addAction("Show/Hide").triggered.connect(self.show_gui)  # open gui
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

        pc = Point_cloud("loaded_points", loaded_points)
        self.widget_canvas.path = QPainterPath()  # clear canvas
        self.update()
        pc.draw_on_canvas()  # drawing loaded stroke
        global points
        points = loaded_points  # allowing "F"

    def set_profile_name(self):
        """ changes the configuration profile name to the new one given by the user"""

        self.label_conf_file.setText(self.lineEdit_profilename.text())
        gv.configuration.profile_name = str(self.lineEdit_profilename.text())
        self.update_file(str(gv.configuration.file_path)+"/"+str(gv.configuration.file_name),
                         0,
                         gv.configuration.profile_name)

    def set_default_conf(self):
        """ restores default configuration"""

        gv.configuration = ConfFromFile()
        self.load_conf()

    def save_conf(self):
        """ save Configuration object content to file"""

        _print("save_conf()")
        fname = QFileDialog.getSaveFileName(self,
                                            "Save Configuration",
                                            "E:\\Documentos\\Estudio\\programming\\Python\\leap\\LEAP_proyect",
                                            "(*.txt)")
        if fname:
            self.save_conf_file(fname)
        else:
            print("error save_conf()")

    def save_conf_file(self, fname):
        """ writes and saves the given file with the configuration info

        :param fname: file path and name to be saved to
        """

        f = open(fname, "w+")

        configuration = gv.configuration
        self.label_conf_file.setText(configuration.profile_name)
        configuration.file_name = str(QFileInfo(fname).fileName())
        configuration.file_path = str(QFileInfo(fname).path())
        configuration.file_date = time.ctime(os.path.getctime(fname))

        f.write(configuration.profile_name + "\n" +
                configuration.file_name + "\n" +
                configuration.file_path + "\n" +
                configuration.file_date + "\n\n")
        f.write(configuration.basic.get_conf())
        f.write("\n")
        f.write(configuration.extra.get_conf())
        f.close()

    def update_file(self, fname, line, replace):
        """ updates a given file name in the given file with the given content

        :param fname: file path and name to be saved to
        :param line: which line to be updated
        :param replace: new content
        """

        with open(fname, "r") as file:
            file_content = file.readlines()

        file_content[line] = replace+str("\n")
        with open(fname, "w") as file:
            file.writelines(file_content)

    def load_conf_file(self):
        """ loads configuration file into Configuration object"""

        _print("load_conf_file()")
        fname = QFileDialog.getOpenFileName(self,
                                            "Save Configuration",
                                            "E:\\Documentos\\Estudio\\programming\\Python\\leap\\LEAP_proyect",
                                            "(*.txt)")
        if fname:
            f = open(fname, "r")
            gv.configuration.load_conf(f)
            self.label_conf_file.setText(gv.configuration.profile_name)

            f.close()

        self.load_conf()

    def load_conf(self):
        """ loads given configuration object into SYSTEM
        updates comboboxes and GUI elements
        using cb_action_gesture array
        """

        _print("load_conf()")

        self.combo_box_mm.setCurrentIndex(int(gv.configuration.basic.mm))

        self.combo_box_click.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_click], gv.configuration.basic.lclick)
        )

        self.combo_box_rclick.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_rclick], gv.configuration.basic.rclick)
        )

        self.combo_box_minimizew.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_minimizew], gv.configuration.basic.minimizew)
        )

        self.combo_box_closew.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_closew], gv.configuration.basic.closew)
        )

        self.combo_box_changew.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_changew], gv.configuration.basic.changew)
        )

        self.combo_box_vscroll.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_vscroll], gv.configuration.basic.vscroll)
        )

        self.combo_box_hscroll.setCurrentIndex(
            get_dict_key(self.cb_action_gesture[self.combo_box_hscroll], gv.configuration.basic.hscroll)
        )

    def debug_mode(self):
        """ opens the canvas window"""

        _print("debug")
        self.canvas.show()

    def show_settings(self):
        """ opens the settings window"""

        _print("settings")
        self.settings.show()

    # Leap status label
    @pyqtSlot(bool)
    def change_leap_status(self, conn):
        """ handles Leap label status on the down bar

        :param conn: true if connected, false if not
        """

        if conn:
            self.label_leap_status.setText("CONNECTED")
            self.label_leap_status.setStyleSheet("QLabel {color: #7FFF00;}")
        else:
            self.label_leap_status.setText("DISCONNECTED")
            self.label_leap_status.setStyleSheet("QLabel {color: #ff3333;}")

    def launch_on_startup(self):
        """ creates shortcut in Startup folder into User's home or removes it
        depending if checkBox is checked or not
        """

        if self.checkBox_startup.isChecked():
            _print("added to startup")
            create_shortcut()
            self.show_popup("Launch on startup",
                            "LEAP MyMouse succesfully added to startup",
                            "")
        else:
            _print("added to startup")
            remove_shortcut()
            self.show_popup("Launch on startup",
                            "LEAP MyMouse succesfully removed from startup",
                            "")

    def keyPressEvent(self, event):
        """ this is a collection of key events binded to GUI

        :param event: pressed key
        """

        global points
        if event.key() == QtCore.Qt.Key_Q:
            self.exit_app()

        elif event.key() == QtCore.Qt.Key_S:
            self.start_stop_control()

        elif event.key() == QtCore.Qt.Key_F:  # start stroke recognition
            if self.n_of_fingers == 1:
                pc = Point_cloud("f1", self.widget_canvas.points, Point(gv.W/4, gv.H/4 + 50, -1))
                # pc.draw_on_canvas()    normalized pc

                result = recognize_stroke(self.widget_canvas.points)
                gesture_match(result.name, "-thread" in sys.argv)

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
                    results.append(recognize_stroke(gv.listener.gesture[c]))
                    gesture_match(results[len(results) - 1].name, "-thread" in sys.argv)

                results_names = [res.name for res in results]
                print(results_names)
                if len(set(results_names)) <= 1:
                    print_score(results[1])
                else:
                    print("inconsistent matches of each finger")

            # resetting values, clearing arrays
            gv.stroke_id = 0
            points = []
            gv.listener.clear_variables()

        elif event.key() == QtCore.Qt.Key_C:  # clear canvas
            _print("clear")
            self.canvas.widget_canvas.clear()
            self.label_score.setText("")

        elif event.key() == QtCore.Qt.Key_G and sys.argv[1] != "-thread":
            # global points
            if self.n_of_fingers == 1:  # recording only 1 finger (index)
                print("1 finger recording mode")
                if gv.listener.capture_frame:  # 2nd "G" press
                    print("record captured")
                    gv.listener.capture_frame = False

                    if self.canvas_algorithm == "NN":
                        # Neural Network recognition selected
                        img_dim = 28
                        matrix = np.zeros((img_dim, img_dim, 3), dtype=np.uint8)
                        white = [255, 255, 255]

                        leap_gesture_points = gv.listener.gesture[1]
                        # undoing convert_to from leap_controller to get min and max
                        for c in range(len(leap_gesture_points)):
                            leap_gesture_points[c].x *= (gv.W / 2)
                            leap_gesture_points[c].x /= gv.W
                            leap_gesture_points[c].y = gv.H - abs(leap_gesture_points[c].y)
                            leap_gesture_points[c].y *= (gv.H / 2)
                            leap_gesture_points[c].y /= gv.H

                        max_leap_y = max(g.y for g in leap_gesture_points)
                        max_leap_x = max((g.x + 200) for g in leap_gesture_points)
                        for c in range(len(leap_gesture_points)):
                            print(leap_gesture_points[c].y),
                            print(leap_gesture_points[c].x)
                            leap_x = leap_gesture_points[c].x + 140
                            leap_y = max_leap_y + 40 - leap_gesture_points[c].y
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
                        leap_gesture_points = gv.listener.gesture[1]
                        pc = Point_cloud("f1", leap_gesture_points).draw_on_canvas()
                        # img = self.matrix_to_img(gv.listener.gesture[1])

                        result = recognize_stroke(leap_gesture_points)
                        gesture_match(result.name, "-thread" in sys.argv)

                        str_accum = "Last/Current gesture points array\n\n"
                        for c in range(0, len(points)):
                            str_accum += "(" + str(points[c].x) + "," + str(points[c].y) + ")"
                            if c != len(points) - 1:
                                str_accum += "\n"

                        print_score(result)
                        self.text_edit.setText(str_accum)

                        # getting finger_1 points
                        points = gv.listener.gesture[1]  # this allows "F" to work with mouse and hand stroke

                else:  # 1st "G" press
                    _print("recording")
                    self.label_count.setText("4")  # countdown after getting gesture
                    # this is like a thread with no wait
                    QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(self.label_count))

            elif self.n_of_fingers == -1:  # recording ALL fingers
                _print("all fingers recording mode")
                aux = -100
                if gv.listener.capture_frame:
                    _print("record captured")
                    gv.listener.capture_frame = False
                    for c in range(0, 5):
                        pc = Point_cloud("f" + str(c), gv.listener.gesture[c], Point(W / 4 + aux, H / 4, -1))
                        pc.draw_on_canvas()
                        aux += 50

                    points = gv.listener.gesture[1]  # just for testing

                else:  # 1st "G" press
                    _print("recording")
                    self.label_count.setText("4")  # countdown after getting gesture
                    # this is like a thread with no wait
                    QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(self.label_count))

    def show_gui(self):
        """ this handles notification area option 'Open/Close'
        hide or shows MainWindow
        """

        _print("show_gui()")

        if self.isVisible():
            self.hide()
        else:
            self.show()

    def matrix_to_img(self, matrix):
        img = Image.fromarray(matrix, "RGB")
        img.thumbnail((28, 28), Image.ANTIALIAS)  # resizing to 28x28
        img.save("image_28x28.png")

        # dilate image
        img = cv2.dilate(cv2.imread("image_28x28.png", cv2.IMREAD_GRAYSCALE),
                         np.ones((3, 3), np.uint8), iterations=1)
        return img

    def neural_network(self, img):
        # setting + normalizing image
        cv2.imshow("image", cv2.resize(img, (200, 200)))
        # img = cv2.resize(img, (8, 8))
        minValueInImage = np.min(img)
        maxValueInImage = np.max(img)
        img = np.floor(np.divide((img - minValueInImage).astype(np.float),
                                 (maxValueInImage - minValueInImage).astype(np.float)) * 16)

        # loading digit database
        digits = datasets.load_digits()
        n_samples = len(digits.images)
        data = digits.images.reshape((n_samples, -1))

        # predict EMNIST
        _print("Loading MLP model from file")
        clf = joblib.load("res/mlp_model.pkl").best_estimator_
        predicted = clf.predict(img.reshape((1, img.shape[0] * img.shape[1])))

        # display results
        _print("prediction: " + str(predicted))
        plt.imshow(img, cmap=plt.cm.gray_r, interpolation="nearest")
        plt.title("result: " + str(predicted))
        plt.show()

    # return str(predicted)

    def recognition_algorithm_ch(self, which):
        """ handles check box selecting recognition algorithm

        :param which: 'pd' or 'NN', p$ algorithm or Neural Network
        """

        _print("canvas algorithm changed to " + str(which))

        if which == "pd":
            self.canvas_algorithm = "pd"
        else:
            self.canvas_algorithm = "NN"

    def combo_box_actiongesture_changed(self, combo_box_name):
        """ collection of key events binded to GUI (configuration tab comboboxes)

        :param combo_box_name: changed combobox variable name
        """

        if combo_box_name == "combo_box_click":
            print("lclick changed" + str(self.combo_box_click.currentIndex()))
            gv.configuration.basic.lclick = self.cb_action_gesture[self.combo_box_click] \
                .get(self.combo_box_click.currentIndex())

        elif combo_box_name == "combo_box_rclick":
            print("rclick changed")
            print(self.cb_action_gesture[self.combo_box_rclick]
                  .get(self.combo_box_rclick.currentIndex()))
            gv.configuration.basic.rclick = self.cb_action_gesture[self.combo_box_rclick] \
                .get(self.combo_box_rclick.currentIndex())

        elif combo_box_name == "combo_box_mm":
            gv.configuration.basic.mm = self.combo_box_mm.currentIndex()

        elif combo_box_name == "combo_box_minimizew":
            gv.configuration.basic.minimizew = self.cb_action_gesture[self.combo_box_minimizew] \
                .get(self.combo_box_minimizew.currentIndex())

        elif combo_box_name == "combo_box_closew":
            gv.configuration.basic.closew = self.cb_action_gesture[self.combo_box_closew] \
                .get(self.combo_box_closew.currentIndex())

        elif combo_box_name == "combo_box_changew":
            gv.configuration.basic.changew = self.cb_action_gesture[self.combo_box_changew] \
                .get(self.combo_box_changew.currentIndex())

        elif combo_box_name == "combo_box_vscroll":
            gv.configuration.basic.vscroll = self.cb_action_gesture[self.combo_box_vscroll] \
                .get(self.combo_box_vscroll.currentIndex())

        elif combo_box_name == "combo_box_hscroll":
            gv.configuration.basic.hscroll = self.cb_action_gesture[self.combo_box_hscroll] \
                .get(self.combo_box_hscroll.currentIndex())

        elif combo_box_name == "combo_box_grabb":
            gv.configuration.basic.grabb = self.cb_action_gesture[self.combo_box_grabb] \
                .get(self.combo_box_grabb.currentIndex())

        elif combo_box_name == "combo_box_showdesktop":
            gv.configuration.extra.show_desktop = self.cb_action_gesture[self.combo_box_showdesktop] \
                .get(self.combo_box_showdesktop.currentIndex())

        elif combo_box_name == "combo_box_openfexplorer":
            gv.configuration.extra.show_explorer = self.cb_action_gesture[self.combo_box_openfexplorer] \
                .get(self.combo_box_openfexplorer.currentIndex())

        elif combo_box_name == "combo_box_copy":
            gv.configuration.extra.copy = self.cb_action_gesture[self.combo_box_copy] \
                .get(self.combo_box_copy.currentIndex())

        elif combo_box_name == "combo_box_paste":
            gv.configuration.extra.paste = self.cb_action_gesture[self.combo_box_paste] \
                .get(self.combo_box_paste.currentIndex())

        elif combo_box_name == "combo_box_cut":
            gv.configuration.extra.cut = self.cb_action_gesture[self.combo_box_cut] \
                .get(self.combo_box_cut.currentIndex())

        self.setFocus()

    def view_gesture(self, combo_box):
        """ loads gesture associated gif

        :param combo_box: gif button associated combobox variable name
        """

        _print("view gesture: " + str(combo_box.currentIndex()))

        self.tab_widget_frames.setCurrentIndex(2)
        print(self.cb_action_gesture.get(combo_box).get(combo_box.currentIndex()))

        self.set_gesture_gif(
            "res/gifs/" + str(self.cb_action_gesture.get(combo_box).get(combo_box.currentIndex())) + ".gif"
        )
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())

    def start_stop_control(self):
        """ this handles the click event to "Start Control" or "Stop Control" into notification
        area icon
        """

        if not gv.listener.status.leap_connected:
            self.show_popup("Problem Detected",
                            "Leap Motion error",
                            "Leap Motion device is not connected")
        else:
            if gv.configuration.check():
                _print("Start/Stop Control")

                if not gv.listener.mouse.active:
                    gv.listener.mouse.active = True
                    self.button_stop.setChecked(False)
                    self.button_stop.setEnabled(True)
                    self.button_start.setChecked(True)

                else:
                    gv.listener.mouse.active = False
                    self.button_start.setChecked(False)
                    self.button_start.setEnabled(True)
                    self.button_stop.setChecked(True)

            else:
                self.show_popup("Problem Detected",
                                "Configuration error",
                                "You have same gesture assigned to multiple actions in your configuration")

    def set_gesture_gif(self, gif):
        """ loads given gif into gif label

        :param gif: .gif file
        """

        giff = QtGui.QMovie(gif)
        self.label_gesture_gif.setMovie(giff)
        giff.start()

    def updateLabel(self, label):
        """ this function handles countdown label"""

        t = int(label.text()) - 1
        if t == 0:
            label.setText("")
            while gv.listener.hand_vel < 270 or gv.listener.fingers_vel[4] < 100:
                pass

            gv.listener.capture_frame = True
            return

        label.setText(str(t))
        QtCore.QTimer.singleShot(1000, lambda: self.updateLabel(label))

    def show_popup(self, title, text, inftext):
        """ displays a pop-up with given information

        :param title: title of the window
        :param text: text into the window
        :param inftext: informative text into the window
        """

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(text)
        msg.setInformativeText(inftext)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def exit_app(self):
        """ ends app execution and closes all windows"""

        _print("exiting...")
        self.close()
        self.opened = False
        sys.exit()
