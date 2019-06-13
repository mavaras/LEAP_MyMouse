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

from PIL import Image
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm
from sklearn import datasets
from sklearn import svm
from sklearn.externals import joblib
from win32api import GetSystemMetrics

# own package imports
from _print import _print
from models.configuration_fromFile import ConfFromFile
from models.PCRecognizer import PCRecognizer
from models.points import Point_cloud

from views.gui_qtdesigner import *
from views.loading_screen import LoadScreen
import views.gui as gui

from controllers.leap_controller import *
from controllers.aux_functions import *

# TODO: features to implement:
#       -> debug mode
#       -> browser with tutorial
#       -> applications interactions (powerpoint, vlc ?)
#       -> gvariables as object ?? (this is good)
#       -> add gifs
#       -> help
#       -> installer with InnoSetup (when exe ready)

# GLOBALS ?
# main_window = None
exit = False

"""
def matrix_to_img(matrix):
    img = Image.fromarray(matrix, "RGB")
    img.thumbnail((28, 28), Image.ANTIALIAS)  # resizing to 28x28
    img.save("image_28x28.png")

    # dilate image
    img = cv2.dilate(cv2.imread("image_28x28.png", cv2.IMREAD_GRAYSCALE),
                     np.ones((3, 3), np.uint8), iterations=1)
    return img


def neural_network(img):
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

    # predict
    print('Loading model from file.')
    clf = joblib.load('mlp_model.pkl').best_estimator_
    predicted = clf.predict(img.reshape((1, img.shape[0] * img.shape[1])))

    # display results
    print("prediction: " + str(predicted))
    plt.imshow(img, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title("result: " + str(predicted))
    plt.show()

    return str(predicted)
"""

'''
# various functions (this shouldn't be here)
def recognize_stroke(points):
    """ this function recognize one SINGLE stroke (if ALL fingers, one by one)"""

    print("recognizing stroke")
    aux = [points]
    result = pcr.recognize(aux)

    return result


def print_score(result):
    """ this shows final score of current stroke (red label on canvas)"""

    score = "Result: matched with " + result.name + " about " + str(round(result.score, 2))
    main_window.label_score.setStyleSheet("color: red")
    main_window.label_score.setText(str(score))
    main_window.text_edit_2.append("\n" + str(score))


def gesture_match(gesture_name):
    """ handling gesture stroke match actions"""

    if gesture_name == "T":
        print("T gesture")
        if "-thread" in sys.argv:
            # handle = win32gui.FindWindow(None, r"Reproductor multimedia VLC")
            hwnd = get_current_window_hwnd()
            if gvariables.configuration.basic.closew == "T":
                close_window(hwnd)
            elif gvariables.configuration.basic.minimizew == "T":
                minimize_window(hwnd)

    elif gesture_name == "V":
        print("V gesture")
        if "-thread" in sys.argv:
            hwnd = get_current_window_hwnd()
            if gvariables.configuration.basic.closew == "V":
                close_window(hwnd)
            elif gvariables.configuration.basic.minimizew == "V":
                minimize_window(hwnd)

    elif gesture_name == "Z":
        print("Z gesture")
        if "-thread" in sys.argv:
            hwnd = get_current_window_hwnd()
            if gvariables.configuration.basic.closew == "Z":
                close_window(hwnd)
            elif gvariables.configuration.basic.minimizew == "Z":
                minimize_window(hwnd)

    elif gesture_name == "W":
        pass

    elif gesture_name == "N":
        pass

    elif gesture_name == "LEFT":
        print("LEFT gesture")
    elif gesture_name == "RIGHT":
        print("RIGHT gesture")
    print("")
'''

'''
# various functions (temporarily here)
def recognize_stroke(points):
    """ this function recognize one SINGLE stroke (if ALL fingers, one by one)

    :params points: points array containing a stroke
    """

    print("recognizing stroke")
    aux = [points]
    result = PCRecognizer().recognize(aux, True)

    return result


def print_score(result):
    """ this shows final score of current stroke (red label on canvas)

    :param result: Result object containing recognition result
    """

    score = "Result: matched with " + result.name + " about " + str(round(result.score, 2))
    gvariables.main_window.label_score.setStyleSheet("color: red")
    gvariables.main_window.label_score.setText(str(score))
    gvariables.main_window.text_edit_2.append("\n" + str(score))


# not updated (not here -> GRecognizer.py)
def gesture_match(gesture_name):
    """ matches gesture_name with its associated action

    :param gesture_name: letter
    """

    print(str(gesture_name) + " gesture\n")
    if "-thread" in sys.argv:
        if gesture_name == gvariables.configuration.basic.closew:
            hwnd = get_current_window_hwnd()
            close_window(hwnd)

        elif gesture_name == gvariables.configuration.basic.minimizew:
            hwnd = get_current_window_hwnd()
            minimize_window(hwnd)

        elif gesture_name == gvariables.configuration.extra.show_desktop:
            hold("windows")
            press("d")
            release("windows")

        elif gesture_name == gvariables.configuration.extra.show_explorer:
            hold("windows")
            press("e")
            release("windows")

        elif gesture_name == gvariables.configuration.extra.copy:
            hold("ctrl")
            press("c")
            release("ctrl")

        elif gesture_name == gvariables.configuration.extra.paste:
            hold("ctrl")
            press("v")
            release("ctrl")

        elif gesture_name == gvariables.configuration.extra.cut:
            hold("ctrl")
            press("x")
            release("ctrl")


def exit_app():
    """ exits applications, closes all windows"""

    print("exiting...")
    global exit
    exit = True
    main_window.close()
    cv2.destroyAllWindows()
    controller.remove_listener(listener)
    sys.exit()


def load_image(path):
    img = cv2.imread(path)
    data = np.array(bytearray(open(path, "rb").read()))
    # img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    height, width, size = img.shape
    step = img.size / height
    qformat = QImage.Format_Indexed8

    if len(img.shape) == 3:
        if size == 4:
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_RGB888

    img = QImage(img, width, height, step, qformat)
    img = img.rgbSwapped()

    return img, height, width
'''


def thread_handler():
    """ this function handles the thread which allows to make "G" + "G" by putting two hands
    on frame (python .py -thread)
    Enables stroke gesture recognition (two hands on frame)
    """

    print("thread_handler_init")
    global exit
    while not exit:
        if gvariables.listener.can_record and \
                not gvariables.listener.capture_frame:
            # here listener.frame_capture is False (we starting a new recording)
            gvariables.listener.recording = True
            time.sleep(.4)
            print("recording")
            while gvariables.listener.hand_vel < 250:
                pass

            gvariables.listener.capture_frame = True

        elif not gvariables.listener.can_record and \
                gvariables.listener.capture_frame:

            """ NEURAL NETWORK CODE
            img_dim = 28
            matrix = np.zeros((img_dim, img_dim, 3), dtype=np.uint8)
            white = [255, 255, 255]
            #leap_gesture_points = gvariables.listener.gesture[1]
            max_leap_y = max(g.y for g in gvariables.listener.gesture[1])
            max_leap_x = max((g.x+200) for g in gvariables.listener.gesture[1])
            
            for c in range(len(gvariables.listener.gesture[1])):
                leap_x = gvariables.listener.gesture[1][c].x + 140
                leap_y = max_leap_y + 40 - gvariables.listener.gesture[1][c].y
                print(str(leap_x)+", "+str(leap_y))
                print(str(leap_x*img_dim/max_leap_x)+"; "+str(leap_y*img_dim/max_leap_y))
                print("")
                matrix_x = int(leap_x*img_dim/max_leap_x)
                matrix_x = 27 if matrix_x == 28 else matrix_x
                matrix_y = int(leap_y*img_dim/max_leap_y)
                matrix_y = 27 if matrix_y == 28 else matrix_y
                matrix[matrix_y][matrix_x] = white
            
            print("max X: "+str(max_leap_x))
            print("max Y: "+str(max_leap_y))
            img = matrix_to_img(matrix)
            pred = neural_network(img).replace("[", "").replace("]", "")
            print("pred: "+str(pred))
            if "Chrome" in get_current_window_name():
                pressHoldRelease("left_control", str(pred))
            """
            print("recording and recognizing captured")
            gvariables.listener.capture_frame = False  # end of Leap capture
            points = gvariables.listener.gesture[1]  # this allows "F" to work with mouse and hand stroke

            if len(points) > 40:
                try:
                    pc = Point_cloud("f1", gvariables.listener.gesture[1])  # pc containing our new gesture
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
            gvariables.listener.clear_variables()
            gvariables.listener.recording = False

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

        elif arg == "-allf":  # ALL fingers capture mode by default
            main_window.combo_box.setCurrentIndex(1)

        elif arg == "-scroll":  # scroll enabled
            gvariables.listener.vscrolling = True
            gvariables.listener.hscrolling = True

        elif arg == "-deepm":  # INTERACTION MODE: deep mode by default
            gvariables.listener.deep_mode = True

        elif arg == "-planem":  # INTERACTION MODE: plane mode by default
            gvariables.listener.plane_mode = True


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
    for c in range(20):
        progress_bar.setValue(c)
        t = time.time()
        while time.time() < t + 0.3:
            app.processEvents()
    time.sleep(1)

    splash.close()


# MAIN BLOCK
if __name__ == "__main__":
    # sys.stdout = gvariables.stdout = ListStream()
    # canvas variables
    result = -1  # result object
    gvariables.pcr = PCRecognizer()  # algorithm class initialization

    # Leap setting up
    listener = leap_listener()
    controller = Leap.Controller()

    # listener initializer
    controller.add_listener(listener)

    # keeping Leap Motion working from background
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    gvariables.listener = listener

    # Configuration
    gvariables.configuration = ConfFromFile()
    gvariables.configuration.check()

    # GUI setting up
    app = QtGui.QApplication([])

    """ls = LoadScreen()
    ls.show()"""

    # show_splash_screen()

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

    gvariables.main_window = gui.MainWindow()

    gvariables.main_window.setFixedSize(gvariables.main_window.size())
    gvariables.main_window.statusBar().setVisible(False)
    gvariables.main_window.initUI()
    gvariables.main_window.show()

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
    gvariables.pcr.templates[5].point_cloud[1].draw_on_canvas(False)
    '''

    app.exec_()
