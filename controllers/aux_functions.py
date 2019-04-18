# -*- coding: utf-8 -*-

# ===============auxiliary functions===============
# == distances
# == sign
# == get dictionary key from its value


import math


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
