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
import webbrowser
import cv2
from PIL import Image
import matplotlib.pyplot as plt  # conflict with sphinx

from sklearn import datasets
from sklearn.externals import joblib

# self package imports
from models.gvariables import gv
from controllers.aux_functions import *
from controllers.configuration_controller import Controller
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

        self.controller = None
        self.configuration = None
        self.listener = None

        self.opened = True
        self.systray = QSystemTrayIcon(QIcon("res/icons/leapmymouse.PNG"), self)

        self.setupUi(self)

    def initUI(self):
        """ widget initialization, positioning, linking etc.
        fills cb_action_gesture array
        """

        self.cvF = Cv_Frame(self)
        self.widget_canvas = None
        self.canvas = Canvas(self)
        self.settings = Settings(self)

        self.set_notification_area()

        self.setWindowIcon(QtGui.QIcon("res/icons/leapmymouse.png"))

        # launch on startup checkbox
        self.checkBox_startup.stateChanged.connect(lambda: self.launch_on_startup())

        # CONFIGURATION TAB

        # label_leap_status default value
        self.change_leap_status(self.listener.status.leap_connected)
        self.listener.status.sgn_leap_connected.connect(self.change_leap_status)

        # cv_frame representation
        self.listener.status.sgn_cv_frame_XY.connect(self.cvF.set_frame_XY)
        self.listener.status.sgn_cv_frame_XZ.connect(self.cvF.set_frame_XZ)

        # Action-gesture COMBOBOXES
        self.combo_box_mm.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_mm"))

        self.combo_box_click.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_click"))

        self.cb_action_gesture[self.combo_box_click] = {0: "click_planem",
                                                        1: "click_deepm",
                                                        2: "click_f2down",
                                                        3: "click_f1down",
                                                        4: "click_f0down"}
        self.cb_action_gesture[self.combo_box_rclick] = {0: "rclick_f2down",
                                                         1: "f1_f2_front",
                                                         2: "rclick_f1down"}

        self.combo_box_minimizew.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_minimizew"))
        self.cb_action_gesture[self.combo_box_minimizew] = {0: "V",
                                                            1: "T",
                                                            2: "W",
                                                            3: "D",
                                                            4: "Z"}
        self.combo_box_rclick.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_rclick"))

        self.combo_box_closew.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_closew"))
        self.cb_action_gesture[self.combo_box_closew] = {0: "T",
                                                         1: "V",
                                                         2: "W",
                                                         3: "Z",
                                                         4: "D"}

        self.combo_box_changew.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_changew"))
        self.cb_action_gesture[self.combo_box_changew] = {0: "90_and_swipe"}

        self.combo_box_vscroll.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_vscroll"))
        self.cb_action_gesture[self.combo_box_vscroll] = {0: "5_fingers_UD",
                                                          1: "5_fingers_LR",
                                                          2: "4_fingers_UD",
                                                          3: "3_fingers_UD"}

        self.combo_box_hscroll.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_hscroll"))
        self.cb_action_gesture[self.combo_box_hscroll] = {0: "default"}

        self.combo_box_grabb.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_grabb"))
        self.cb_action_gesture[self.combo_box_grabb] = {0: "f1_f2"}

        self.combo_box_showdesktop.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_showdesktop"))
        self.cb_action_gesture[self.combo_box_showdesktop] = {0: "D",
                                                              1: "T",
                                                              2: "V",
                                                              3: "Z",
                                                              4: "W"}

        self.combo_box_openfexplorer.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_openfexplorer"))
        self.cb_action_gesture[self.combo_box_openfexplorer] = {0: "X",
                                                                1: "Z",
                                                                2: "D",
                                                                3: "V",
                                                                4: "W"}

        self.combo_box_copy.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_copy"))
        self.cb_action_gesture[self.combo_box_copy] = {0: "Z",
                                                       1: "D",
                                                       2: "T",
                                                       3: "V",
                                                       4: "W"}

        self.combo_box_paste.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_paste"))
        self.cb_action_gesture[self.combo_box_paste] = {0: "L",
                                                        1: "T",
                                                        2: "Z",
                                                        3: "D",
                                                        4: "W"}

        self.combo_box_cut.currentIndexChanged["int"].connect(
            lambda: self.controller.combo_box_actiongesture_changed("combo_box_cut"))
        self.cb_action_gesture[self.combo_box_cut] = {0: "W",
                                                      1: "X",
                                                      2: "D",
                                                      3: "Z",
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
        self.button_setprofilename.clicked.connect(lambda: self.controller.set_profile_name(self.lineEdit_profilename.text()))
        self.lineEdit_profilename.setText("")

        self.button_stop.setChecked(True)
        self.button_stop.clicked.connect(lambda: self.controller.start_stop_control())
        self.button_start.setChecked(False)
        self.button_start.clicked.connect(lambda: self.controller.start_stop_control())

        # MENUBAR
        self.menubar_file_loadconf.triggered.connect(self.load_conf)
        self.menubar_file_saveconf.triggered.connect(self.save_conf)
        self.menubar_file_loaddefconf.triggered.connect(self.set_default_conf)
        self.menubar_help_debug.triggered.connect(self.debug_mode)
        self.menubar_help_settings.triggered.connect(self.show_settings)
        self.menubar_help_help.triggered.connect(self.show_help)

    def set_notification_area(self):
        """ this function sets notification area menu"""

        self.systray.show()
        self.systray.showMessage("LEAP MyMouse",
                                 "App working",
                                 QSystemTrayIcon.NoIcon)
        # right click options
        self.systray_menu = QMenu(self)
        self.opt_startcontrol = self.systray_menu.addAction("Show/Hide").triggered.connect(self.show_gui)  # open gui
        self.opt_startcontrol = self.systray_menu.addAction("Start Control").triggered.connect(self.controller.start_stop_control)
        self.opt_stopcontrol = self.systray_menu.addAction("Stop Control").triggered.connect(self.controller.start_stop_control)
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

    def set_default_conf(self):
        """ restores default configuration"""

        self.configuration = ConfFromFile()  # reset conf
        self.controller.load_conf()

    def save_conf(self):
        """ save Configuration object content to file"""

        self._print("save_conf()")
        fname = QFileDialog.getSaveFileName(self,
                                            "Save Configuration",
                                            os.getcwd(),
                                            "(*.txt)")
        if fname:
            self.controller.save_conf_file(fname)
            self.label_conf_file.setText(self.configuration.profile_name)

        else:
            print("error save_conf()")

    def load_conf(self):
        self._print("load_conf()")
        fname = QFileDialog.getOpenFileName(self,
                                            "Load Configuration",
                                            os.getcwd(),
                                            "(*.txt)")
        if fname:
            self.controller.load_conf_file(fname)
            self.label_conf_file.setText(self.configuration.profile_name)

        self.controller.load_conf()

    def debug_mode(self):
        """ opens the canvas window"""

        self._print("debug")
        self.canvas.show()

    def show_settings(self):
        """ opens the settings window"""

        self._print("settings")
        self.settings.show()

    def show_help(self):
        """ opens a browser tab with the technical documentation of the proyect"""

        webbrowser.open("mavaras.github.io/leapmymouse_docs", new=2)

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
            self._print("added to startup")
            create_shortcut(self.configuration.startup_path)
            self.show_popup("Launch on startup",
                            "LEAP MyMouse successfully added to startup",
                            "")
        else:
            self._print("added to startup")
            remove_shortcut(self.configuration.startup_path)
            self.show_popup("Launch on startup",
                            "LEAP MyMouse successfully removed from startup",
                            "")

    def keyPressEvent(self, event):
        """ this is a collection of key events binded to GUI

        :param event: pressed key
        """

        global points
        if event.key() == QtCore.Qt.Key_Q:
            self.exit_app()

        elif event.key() == QtCore.Qt.Key_S:
            self.controller.start_stop_control()

    def show_gui(self):
        """ this handles notification area option 'Open/Close'
        hide or shows MainWindow
        """

        self._print("show_gui()")

        if self.isVisible():
            self.hide()
        else:
            self.show()

    def recognition_algorithm_ch(self, which):
        """ handles check box selecting recognition algorithm

        :param which: 'pd' or 'NN', p$ algorithm or Neural Network
        """

        self._print("canvas algorithm changed to " + str(which))

        if which == "pd":
            self.canvas_algorithm = "pd"
        else:
            self.canvas_algorithm = "NN"

    def view_gesture(self, combo_box):
        """ loads gesture associated gif

        :param combo_box: gif button associated combobox variable name
        """

        self._print("view gesture: " + str(combo_box.currentIndex()))

        self.tab_widget_frames.setCurrentIndex(2)
        print(self.cb_action_gesture.get(combo_box).get(combo_box.currentIndex()))

        self.set_gesture_gif(
            "res/gifs/" + str(self.cb_action_gesture.get(combo_box).get(combo_box.currentIndex())) + ".gif"
        )
        self.label_gesture_gif.setLayout(QtGui.QHBoxLayout())

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
            while self.listener.hand_vel < 270 or self.listener.fingers_vel[4] < 100:
                pass

            self.listener.capture_frame = True
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

    def _print(self, string):
        print(string)
        gv.stdout += "__> "+string+"\n"
        self.textArea_logs.setPlainText(gv.stdout)

    def exit_app(self):
        """ ends app execution and closes all windows"""

        self._print("exiting...")

        self.close()
        self.opened = False
        sys.exit()
