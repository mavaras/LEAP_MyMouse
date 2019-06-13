# -*- coding: utf-8 -*-

# ===============auxiliary functions===============
# == distances
# == sign
# == get dictionary key from its value
# == gesture classification functions


import math
from win32_functions import *
import gvariables
from key_handle import *


# sign = lambda a: (a > 0) - (a < 0)
def sign(n):
    """ return the sign of given number
    :param n: number
    :return: -1 or 1
    """
    return n // abs(n)


def distance_3d(x, y, z, x2, y2, z2):
    """ calculates the 3d distance between two given points
    :param x: point1 x
    :param y: point1 y
    :param z: point1 z
    :param x2: point2 x
    :param y2: point2 y
    :param z2: point2 z
    :return: 3d distance between point1 and point2
    """
    return math.sqrt(abs(x - x2) + abs(y - y2) + abs(z - z2))


def distance(p1, p2):
    """ calculates 2d distance between p1 and p2
    :param p1: point 1
    :param p2: point 2
    :return: 2d distance between point1 and point2
    """
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt(dx * dx + dy * dy)


def get_dict_key(dic, value):
    """ returns given dictionary key corresponding to given value

    :param dic: dictionary
    :param value: value which key is returned
    :return: key which value into dic is value
    """
    # print(value),
    # print(dic)
    return [key for key in dic.keys() if dic[key] == str(value)][0]


def recognize_stroke(points):
    """ this function recognize one SINGLE stroke (if ALL fingers, one by one)

    :param points: points array containing a stroke
    """

    print("recognizing stroke")
    aux = [points]
    result = gvariables.pcr.recognize(aux, True)

    return result


def print_score(result):
    """ this shows final score of current stroke (red label on canvas)

    :param result: Result object containing recognition result
    """

    score = "Result: matched with " + result.name + " about " + str(round(result.score, 2))
    gvariables.main_window.canvas.label_score.setStyleSheet("color: white; font-size: 12pt;")
    gvariables.main_window.canvas.label_score.setText(str(score))
    # gvariables.main_window.canvas.text_edit_2.append("\n" + str(score))


# not updated (not here -> GRecognizer.py)
def gesture_match(gesture_name, active=True):
    """ matches gesture_name with its associated action

    :param gesture_name: letter
    """
    print(str(gesture_name) + " gesture\n")

    if active:
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
