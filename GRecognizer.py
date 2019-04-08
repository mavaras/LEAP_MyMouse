# -*- coding: utf-8 -*-

# ===============MAIN FILE===============
# == initializations
# ==== view
# ==== leap_controller
# ==== configuration
# ==== win32
# == threads


# basic modules imports
import time
import ctypes
import sys
import os
import math
import numpy as np
import threading

# aux modules imports
import win32api, win32con, win32gui
import cv2
import linecache2 as linecache
from collections import deque

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PIL import Image
import matplotlib.pyplot as plt
from scipy.misc import imresize
from sklearn import datasets
from sklearn import svm

# own package imports
import gvariables

from models.configuration import *
from models.PCRecognizer import PCRecognizer
from models.points import Point_cloud

from views.gui_qtdesigner import *
import views.gui as gui

from controllers.leap_controller import *
from controllers.win32_functions import *
from controllers.aux_functions import *

# TODO: features to implement:
#       -> launch on startup
#       -> extra conf
#       -> add gifs
#       -> help
#       -> notification area

# GLOBALS ?
# main_window = None
exit = False


def matrix_to_img(matrix):
    img = Image.fromarray(matrix, "RGB")
    # img.thumbnail((28, 28), Image.ANTIALIAS)  # resizing to 28x28
    img.save("image_28x28.png")
    # img.show()

    # dilate image
    img = cv2.imread("image_28x28.png", cv2.IMREAD_GRAYSCALE)
    img = cv2.dilate(img, np.ones((3, 3), np.uint8), iterations=2)
    # img = cv2.erode(img, np.ones((3, 3), np.uint8), iterations=1)

    return img


def neural_network(img):
    # setting + normalizing image
    # cv2.imshow("image", cv2.resize(img, (200, 200)))
    img = np.delete(img, np.where(~img.any(axis=1))[0], axis=0)
    img = np.delete(img, np.where(~img.any(axis=0))[0], axis=1)
    img = cv2.resize(img, (8, 8))
    minValueInImage = np.min(img)
    maxValueInImage = np.max(img)
    img = np.floor(
        np.divide((img - minValueInImage).astype(np.float), (maxValueInImage - minValueInImage).astype(np.float)) * 16)
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
    print("prediction: " + str(predicted))
    plt.imshow(img, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title("result: " + str(predicted))
    # plt.show()

    return str(predicted)


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


def thread_handler():
    """ this function handles the thread which allows to make "G" + "G" by putting two hands
    on frame (python .py -thread)
    Enables stroke gesture recognition (two hands on frame)
    """

    print("thread_handler_init")
    global exit
    while not exit:
        if len(gvariables.listener.frame.hands) == 2 and not gvariables.listener.capture_frame:
            # here listener.frame_capture is False (we starting a new recording)
            time.sleep(.5)
            print("recording")
            while (gvariables.listener.hand_vel < 270):
                pass

            gvariables.listener.capture_frame = True

        elif len(gvariables.listener.frame.hands) == 1 and gvariables.listener.capture_frame:
            print("recording and recognizing captured")
            gvariables.listener.capture_frame = False  # end of Leap capture
            pc = Point_cloud("f1", gvariables.listener.gesture[1])  # pc containing our new gesture
            pc.draw_on_canvas()  # drawing pc on canvas to see the shape

            global points, stroke_id
            points = gvariables.listener.gesture[1]  # this allows "F" to work with mouse and hand stroke
            listener.c = 0

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

            result = recognize_stroke(points)
            gesture_match(result.name)
            gui.print_score(result)

            stroke_id = 0  # reseting values
            points = []
            gvariables.listener.clear_variables()

    print("thread_handler_end")


def console_args(args):
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


# MAIN BLOCK	
if __name__ == "__main__":
    print(sys.platform)
    # canvas variables
    points = gvariables.points  # where to store drawn points
    stroke_id = gvariables.stroke_id
    result = -1  # result object
    pcr = PCRecognizer()  # algorithm class initialization

    # Leap setting up
    listener = leap_listener()
    controller = Leap.Controller()

    # listener initializer
    controller.add_listener(listener)

    # keeping Leap Motion working from background
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    gvariables.listener = listener

    # Configuration
    gvariables.configuration = Conf()

    # GUI setting up
    app = QtGui.QApplication([])
    gvariables.main_window = gui.MainWindow()
    gvariables.main_window.initUI()
    gvariables.main_window.show()

    console_args(sys.argv)

    # win32 stuff
    opened_windows_names = []
    opened_windows_names = get_opened_windows_list()

    print("currently opened windows")
    print(opened_windows_names)  # .encode("utf-8")
    # print("-> "+opened_windows_names[8])
    print(get_current_window_name())

    # drawing tests
    #pcr.templates[4].point_cloud[0].draw_on_canvas(False)

    app.exec_()
