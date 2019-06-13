# -*- coding: utf-8 -*-

import gvariables
from PCRecognizer_functions import *
from PyQt4 import QtCore


class Point:
    """ this CLASS represents a single point into a place or stroke
    :param x: x coordinate
    :param y: y coordinate
    :param id: id of the point (stroke id)

    """

    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    def convert_to(self, where_W, where_H):
        """ translates Point coordinates to different dimensions place (Leap coordinates)
        Inverts Y coordinate.

        :param where_W: width of new place
        :param where_H: height of new place
        """
        self.y = where_H - abs(self.y)  # Y inversion
        self.x = (W * self.x) / where_W
        self.y = (H * self.y) / where_H

    """def draw_on_canvasTK(self, radius):
        canvas.create_oval(self.x - radius, self.y - radius,
                           self.x + radius, self.y + radius, fill="#aaaaaa")"""

    def draw_on_canvas(self, radius, path):
        """ draws Point on GUI Canvas as a circle

        :param radius: radius of the circle
        :param path: widget_canvas's path (colour)
        """
        eval("gvariables.main_window.canvas.widget_canvas." + path +
             ".addEllipse(QtCore.QRectF(self.x, self.y, radius, radius))")
        gvariables.main_window.widget_canvas.update()


class Point_cloud:
    """ this CLASS represents a cloud of points
    point cloud = collection of points defining a shape, it's like a points array

    :param name: name of the point cloud
    :param points: Point array
    :param where_to_translate: special cases (has a default value)
    """

    def __init__(self, name, points, where_to_translate=Point(W/4, H/4, -1)):
        self.origin = where_to_translate
        self.name = name
        self.points = resample(points, 32)  # point cloud resizing
        self.points = scale(self.points)  # point cloud scaling
        self.points = translate_to(self.points, self.origin)  # point cloud centering

    def draw_on_canvas(self, flag=True):
        """ draws Point_cloud on GUI Canvas

        :param flag: if is true we are drawing various fingers (different colours)
        """
        # aux_points = []  to not overwriting original self.points array
        aux_points = amplify(self.points, 200)  # kind of scale reversion
        aux_points = translate_to(aux_points,
                                  Point(self.origin.x, self.origin.y / 2, -1))  # translating amplilfied pc to center
        dic = {"f0": "path_points_0", "f1": "path_points_1",
               "f2": "path_points_2", "f3": "path_points_3", "f4": "path_points_4"}

        # aux_points = points
        c = 0
        if flag:
            path = dic.get(self.name)
        else:  # black color by default
            path = "path_points_1"

        for p in aux_points:
            if c == num_points:
                # last point
                p.draw_on_canvas(10, path)
            else:
                p.draw_on_canvas(6, path)

            c += 1
