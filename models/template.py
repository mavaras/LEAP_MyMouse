# -*- coding: utf-8 -*-

# ===============Template CLASS===============
# == Template class
# == loads predefined templates


from models.Point import Point
from models.Point_cloud import Point_cloud


class Template:
    """ this CLASS represents a full Template, that's it a template representing a form (name)
    but with some different ways of representing it (point_cloud array)
    """

    def __init__(self, name, point_cloud, fingers_point_cloud):
        self.name = name
        self.point_cloud = point_cloud
        self.fingers_point_cloud = fingers_point_cloud  # this if template is a complex one


def init_templates():
    """  initialize templates array for PCRecognizer class

    :return: templates array
    """

    templates = []

    # single stroke templates (all fingers doing the same if various fingers) (1 finger)
    templates.append(Template("T", [
        # different PC for having different ways of drawing Template.name (T) for better recognition
        Point_cloud("T1", [Point(30, 7, 1), Point(103, 7, 1),
                              Point(66, 7, 2), Point(66, 87, 2)])
        ,
        Point_cloud("T2", [Point(30, 7, 1), Point(123, 7, 1),
                              Point(80, 17, 2), Point(30, 7, 2),
                              Point(80, 17, 3), Point(80, 77, 3)])
        ,
        Point_cloud("T3", [Point(30, 7, 1), Point(123, 7, 1),
                              Point(80, 17, 2), Point(30, 7, 2),
                              Point(80, 17, 3), Point(80, 50, 3)])
        ], None)
    )
    templates.append(Template("V", [
        Point_cloud("V1", [Point(30, 7, 1), Point(40, 37, 1),
                              Point(40, 37, 2), Point(50, 7, 2)])
        ,
        Point_cloud("V2", [Point(0, 7, 1), Point(25, 37, 1),
                              Point(25, 37, 2), Point(50, 7, 2)])
        ,
        Point_cloud("V3", [Point(30, 7, 1), Point(40, 25, 1),
                              Point(40, 25, 2), Point(50, 7, 2)])
        ,
        Point_cloud("V4", [Point(30, 16, 1), Point(33, 25, 1),
                              Point(33, 25, 2), Point(38, 7, 2)])
        ,
        Point_cloud("V5", [Point(30, 7, 1), Point(33, 25, 1),
                              Point(33, 25, 2), Point(38, 16, 2)])
        ], None)
    )
    templates.append(Template("D", [
        Point_cloud("D1", [Point(30, 7, 1), Point(30, 67, 1),
                              Point(30, 67, 2), Point(50, 53, 2),
                              Point(50, 53, 3), Point(55, 37, 3),
                              Point(55, 37, 4), Point(50, 21, 4),
                              Point(50, 21, 5), Point(30, 7, 5)])
        ,
        Point_cloud("D1", [Point(30, 7, 1), Point(30, 67, 1),
                              Point(30, 67, 2), Point(60, 53, 2),
                              Point(60, 53, 3), Point(65, 37, 3),
                              Point(65, 37, 4), Point(60, 21, 4),
                              Point(60, 21, 5), Point(30, 7, 5)])
        ,
        ], None)
    )
    templates.append(Template("X", [
        Point_cloud("X1", [Point(30, 7, 1), Point(60, 47, 1),
                              Point(60, 7, 2), Point(30, 47, 2)])
        ,
        Point_cloud("X1_2", [Point(30, 7, 1), Point(60, 34, 1),
                                Point(60, 7, 2), Point(30, 34, 2)])
        ,
        Point_cloud("X2", [Point(30, 7, 1), Point(60, 47, 1),
                              Point(60, 7, 2), Point(30, 47, 2),
                              Point(30, 7, 3), Point(60, 7, 3)])
        ,
        Point_cloud("X3", [Point(30, 7, 1), Point(60, 47, 1),
                              Point(60, 7, 2), Point(30, 47, 2),
                              Point(30, 47, 3), Point(60, 47, 3)])
        ,
        Point_cloud("X4", [Point(30, 7, 1), Point(60, 47, 1),
                              Point(60, 7, 2), Point(30, 47, 2),
                              Point(30, 7, 3), Point(30, 47, 3)])
        ], None)
    )
    templates.append(Template("W", [
        Point_cloud("W1", [Point(30, 7, 1), Point(40, 37, 1),
                              Point(40, 37, 2), Point(50, 20, 2),
                              Point(50, 20, 3), Point(60, 37, 3),
                              Point(60, 37, 4), Point(70, 7, 4)])
        ,
        Point_cloud("W2", [Point(30, 7, 1), Point(50, 37, 1),
                              Point(50, 37, 2), Point(70, 7, 2),
                              Point(70, 7, 3), Point(90, 37, 3),
                              Point(90, 37, 4), Point(110, 7, 4)])
        ], None)
    )

    templates.append(Template("L", [
        Point_cloud("L1", [Point(30, 27, 1), Point(30, 37, 1),
                              Point(30, 37, 2), Point(40, 37, 2)])
        ,
        Point_cloud("L2", [Point(30, 17, 1), Point(30, 37, 1),
                              Point(30, 37, 2), Point(40, 37, 2)])
        ], None)
    )
    templates.append(Template("Z", [
        Point_cloud("Z1", [Point(30, 7, 1), Point(60, 7, 1),
                              Point(60, 7, 2), Point(30, 27, 2),
                              Point(30, 27, 3), Point(60, 27, 3)])
        ,
        Point_cloud("Z2", [Point(30, 7, 1), Point(50, 12, 1),
                              Point(50, 12, 2), Point(30, 35, 2),
                              Point(30, 35, 3), Point(55, 30, 3)])
        ,
        Point_cloud("Z3", [Point(30, 7, 1), Point(50, 12, 1),
                              Point(50, 12, 2), Point(20, 37, 2),
                              Point(20, 37, 3), Point(52, 33, 3)])
        ,
        Point_cloud("Z4", [Point(30, 21, 1), Point(50, 8, 1),
                              Point(50, 8, 2), Point(23, 30, 2),
                              Point(23, 30, 3), Point(54, 27, 3)])
        ,
        Point_cloud("Z5", [Point(40, 7, 1), Point(60, 7, 1),
                              Point(60, 7, 2), Point(30, 25, 2),
                              Point(30, 25, 3), Point(70, 27, 3)])
        ,
        Point_cloud("Z6", [Point(20, 7, 1), Point(70, 7, 1),
                              Point(70, 7, 2), Point(30, 28, 2),
                              Point(30, 28, 3), Point(57, 27, 3)])
        ], None)
    )

    return templates
