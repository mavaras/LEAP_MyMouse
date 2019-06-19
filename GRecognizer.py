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

# aux modules imports
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from win32api import GetSystemMetrics

# own package imports
from _print import _print
from models.configuration_fromFile import ConfFromFile
from models.PCRecognizer import PCRecognizer
from models.points import Point_cloud

from views.gui_qtdesigner import *
import views.gui as gui


from controllers.leap_controller import *
from controllers.aux_functions import *

# TODO: features to implement:
#       -> browser with tutorial
#       -> add gifs
#       -> help
#       -> installer with InnoSetup (when exe ready)

exit = False


def thread_handler():
    """ this function handles the thread which allows to make "G" + "G" by putting two hands
    on frame (python .py -thread)
    Enables stroke gesture recognition (two hands on frame)
    """

    print("thread_handler_init")
    global exit
    while not exit:
        if gv.listener.can_record and \
                not gv.listener.capture_frame:
            # here listener.frame_capture is False (we starting a new recording)
            gv.listener.recording = True
            time.sleep(.4)
            print("recording")
            while gv.listener.hand_vel < 250:
                pass

            gv.listener.capture_frame = True

        elif not gv.listener.can_record and \
                gv.listener.capture_frame:

            print("recording and recognizing captured")
            gv.listener.capture_frame = False  # end of Leap capture
            points = gv.listener.gesture[1]  # this allows "F" to work with mouse and hand stroke
            print("_>"+str(len(points)))
            if len(points) > 20:
                try:
                    pc = Point_cloud("f1", gv.listener.gesture[1])  # pc containing our new gesture
                    pc.draw_on_canvas()  # drawing pc on canvas to see the shape
                except:
                    print("some point_cloud error...")

                try:
                    result = recognize_stroke(points)
                    gesture_match(result.name)
                    print("score: " + str(result.score))
                # print_score(result)
                except:
                    print("u have to redo the gesture")

            stroke_id = 0  # reseting values
            points = []
            gv.listener.clear_variables()
            gv.listener.recording = False

    print("thread_handler_end")


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

    timer = QtCore.QElapsedTimer()
    timer.start()

    time.sleep(1)
    for c in range(15):
        progress_bar.setValue(c)
        t = time.time()
        while time.time() < t + 0.3:
            app.processEvents()

    time.sleep(1)

    splash.close()


# MAIN BLOCK
if __name__ == "__main__":
    from gvariables import gv

    gv.pcr = PCRecognizer()  # algorithm class initialization

    # Leap set up
    listener = leap_listener()
    controller = Leap.Controller()

    # listener initializer
    controller.add_listener(listener)

    # keeping Leap Motion working from background
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    gv.listener = listener

    # Configuration
    gv.configuration = ConfFromFile()
    gv.configuration.check()

    # GUI setting up
    app = QtGui.QApplication([])

    """ls = LoadScreen()
    ls.show()"""

    show_splash_screen()

    """font = QtGui.QFont('Helvetica', 12, QtGui.QFont.Normal)
    font.setPointSize(12)
    app.setFont(font)"""

    """for key in QtGui.QStyleFactory.keys():
        st = QtGui.QStyleFactory.create(key)
        print(key, st.metaObject().className(), type(app.style()))"""

    # app.setStyle("Plastique")

    id = QtGui.QFontDatabase.addApplicationFont("res/fonts/OpenSans-Regular.ttf")

    stylesheet = open('res/MaterialDark.qss').read()
    stylesheet = stylesheet.replace("color_hover", "#04B97F")
    stylesheet = stylesheet.replace("color_main", "#252323")
    stylesheet = stylesheet.replace("color_label", "#EDEBE1")  # "#949EA2")
    '''
    stylesheet = stylesheet.replace("@color1", "#84A462")  # back
    stylesheet = stylesheet.replace("@color2", "#555639")  # scrollareas
    stylesheet = stylesheet.replace("@color3", "#ECEA89")  # main
    stylesheet = stylesheet.replace("@color4", "#25372B")  # rare
    stylesheet = stylesheet.replace("@color5", "#B39963")  # tabs
    stylesheet = stylesheet.replace("@label", "#ECEA89")
    stylesheet = stylesheet.replace("@button_hover", "#84A462")
    stylesheet = stylesheet.replace("@cb_hover", "#84A462")
    
    stylesheet = stylesheet.replace("@color1", "#F7F8F7")
    stylesheet = stylesheet.replace("@color2", "#F7F8F7")
    stylesheet = stylesheet.replace("@color3", "#A1A363")
    stylesheet = stylesheet.replace("@color4", "#A3444A")
    stylesheet = stylesheet.replace("@color5", "#EEDB6B")
    stylesheet = stylesheet.replace("@label", "#000")
    stylesheet = stylesheet.replace("@button_hover", "#A3444A")
    stylesheet = stylesheet.replace("@cb_hover", "#A3444A")
    '''
    app.setStyleSheet(stylesheet)

    main_window = gui.MainWindow()

    main_window.setFixedSize(main_window.size())
    main_window.statusBar().setVisible(False)
    main_window.initUI()
    main_window.show()

    gv.main_window = main_window

    console_args(sys.argv)

    _print("SYSTEM started")
    _print("sys platform: " + str(sys.platform))
    _print(str(GetSystemMetrics(0)) + ", " + str(GetSystemMetrics(1)))

    '''
    # win32 stuff
    opened_windows_names = []
    opened_windows_names = get_opened_windows_list()

    print("currently opened windows")
    print(opened_windows_names)  # .encode("utf-8")
    # print("-> "+opened_windows_names[8])
    print(get_current_window_name())

    # drawing tests
    gv.pcr.templates[5].point_cloud[1].draw_on_canvas(False)
    '''

    app.exec_()
