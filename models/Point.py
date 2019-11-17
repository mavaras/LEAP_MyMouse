# -*- coding: utf-8 -*-

from models.gvariables import gv


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
        self.x = (gv.W * self.x)/where_W
        self.y = (gv.H * self.y)/where_H

    """def draw_on_canvasTK(self, radius):
        canvas.create_oval(self.x - radius, self.y - radius,
                           self.x + radius, self.y + radius, fill="#aaaaaa")"""

    def draw_on_canvas(self, radius, path):
        """ draws Point on GUI Canvas as a circle

        :param radius: radius of the circle
        :param path: widget_canvas's path (colour)
        """

        eval("gv.main_window.canvas.widget_canvas." + path +
             ".addEllipse(QtCore.QRectF(self.x, self.y, radius, radius))")
        gv.main_window.widget_canvas.update()
