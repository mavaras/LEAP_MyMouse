# -*- coding: utf-8 -*-

# ===============MAIN FILE===============
# == initializations
# ==== view
# ==== leap_controller
# ==== configuration
# ==== win32
# == threads


# basic modules imports
import sys
import threading
import time
import os

# aux modules imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar

# from win32api import GetSystemMetrics

# own package imports
from models.configuration_fromFile import ConfFromFile
from models.PCRecognizer import PCRecognizer
from models.Point_cloud import Point_cloud

from views.gui_qtdesigner import *
import views.gui as gui

from controllers.leap_controller import *
from controllers.utils import *
from controllers.configuration_controller import Controller


def init_thread():
    """ inits gesture recognition thread"""

    thread = threading.Thread(target=thread_handler)
    thread.setDaemon(True)
    thread.start()


def thread_handler():
    """ this function handles the thread which allows to make "G" + "G" by putting two hands
    on frame (python .py -thread)
    Enables stroke gesture recognition (two hands on frame)
    """

    print("thread_handler_init")
    while True:
        try:
            if listener.can_record and not listener.capture_frame:
                listener.recording = True
                time.sleep(.4)
                print("recording")
                while listener.hand_vel < 250:
                    pass

                listener.capture_frame = True

            elif not listener.can_record and \
                    listener.capture_frame:

                print("recording and recognizing captured")
                listener.capture_frame = False  # end of Leap capture
                points = listener.gesture[1]  # this allows "F" to work with mouse and hand stroke
                if len(points) > 20:
                    try:
                        pc = Point_cloud("f1", listener.gesture[1])  # pc containing our new gesture
                        pc.draw_on_canvas()  # drawing pc on canvas to see the shape
                    except:
                        print("some point_cloud error...")

                    try:
                        result = recognize_stroke(points)
                        gesture_match(result.name, conf)
                    except:
                        print("u have to redo the gesture")

                listener.clear_variables()
                listener.recording = False

        except:
            pass


def console_args(args):
    """ handles console arguments input

    :param args: array of arguments
    """

    # shell arguments
    for arg in args:
        if arg == "-thread":  # no keys gesture recognition enabled
            thread = threading.Thread(target=thread_handler)
            thread.setDaemon(True)
            thread.start()


def show_splash_screen():
    """ displays splash screen before loading main window"""

    splash_pix = QPixmap("res/logo.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())

    progress_bar = QProgressBar(splash)
    progress_bar.setMaximum(20)
    progress_bar.setGeometry(130,
                             splash_pix.height() - 50,
                             splash_pix.width() - 240,
                             20)
    progress_bar.setStyleSheet("""
        QProgressBar {
            border: 1px solid #252323;
            border-radius: 6px;
            text-align: center;
            position: center;
            background-color: #252323;
            font-size: 1px;
        }

        QProgressBar::chunk {
            background-color: #04B97F;
            border-radius: 9px;
            margin-right: 23px;
            width: 20px;
        }""")

    splash.show()

    timer = QElapsedTimer()
    timer.start()

    time.sleep(1)
    for c in range(20):
        progress_bar.setValue(c)
        t = time.time()
        while time.time() < t + 0.3:
            app.processEvents()

    time.sleep(1)

    splash.close()


# MAIN BLOCK
if __name__ == "__main__":
    # Configuration
    conf = ConfFromFile()
    conf.startup_path = str(os.path.expanduser("~"))+"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    conf.check()

    # GUI setting up
    app = QApplication([])
    screen_resolution = app.desktop().screenGeometry()


    # GUI style
    stylesheet = open("res/MaterialDark.qss").read()
    stylesheet = stylesheet.replace("color_hover", "#04B97F")
    stylesheet = stylesheet.replace("color_main", "#252323")
    stylesheet = stylesheet.replace("color_label", "#EDEBE1")
    app.setStyleSheet(stylesheet)

    # MVC setup
    listener = leap_listener()
    listener.configuration = conf
    leap_controller = Leap.Controller()
    leap_controller.add_listener(listener)
    leap_controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)  # keeping Leap Motion working from background

    show_splash_screen()

    main_window = gui.MainWindow()
    main_window.listener = listener
    controller = Controller(main_window, listener, conf)
    main_window.initUI()

    listener.view = main_window

    gv.pcr = PCRecognizer()

    init_thread()

    main_window._print("SYSTEM started")
    main_window._print("sys platform: " + str(sys.platform))

    app.exec_()
