# -*- coding: utf-8 -*-

from models.gvariables import gv
from models.PCRecognizer_functions import resample, amplify, scale, num_points, translate_to
from models.Point import Point


class Point_cloud:
    """ this CLASS represents a cloud of points
    point cloud = collection of points defining a shape, it's like a points array

    :param name: name of the point cloud
    :param points: Point array
    :param where_to_translate: special cases (has a default value)
    """

    def __init__(self, name, points, where_to_translate=Point(gv.W/4, gv.H/4, -1)):
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
                                  Point(self.origin.x, self.origin.y/2, -1))  # translating amplilfied pc to center
        dic = {"f0": "path_points_0", "f1": "path_points_1",
               "f2": "path_points_2", "f3": "path_points_3", "f4": "path_points_4"}

        c = 0
        if flag:
            path = dic.get(self.name)
        else:
            path = "path_points_1"  # black color by default

        for p in aux_points:
            if c == num_points:
                # last point
                p.draw_on_canvas(10, path)
            else:
                p.draw_on_canvas(6, path)

            c += 1
