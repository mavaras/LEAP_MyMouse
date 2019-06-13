# -*- coding: utf-8 -*-

# ===============Template CLASS===============
# == Template class
# == loads predefined templates


import points as ps


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
        # Template point clouds
        # different ways of drawing Template.name (T) for better recognition
        ps.Point_cloud("T1", [ps.Point(30, 7, 1), ps.Point(103, 7, 1),
                              ps.Point(66, 7, 2), ps.Point(66, 87, 2)])
        ,
        ps.Point_cloud("T2", [ps.Point(30, 7, 1), ps.Point(123, 7, 1),
                              ps.Point(80, 17, 2), ps.Point(30, 7, 2),
                              ps.Point(80, 17, 3), ps.Point(80, 77, 3)])
        ,
        ps.Point_cloud("T3", [ps.Point(30, 7, 1), ps.Point(123, 7, 1),
                              ps.Point(80, 17, 2), ps.Point(30, 7, 2),
                              ps.Point(80, 17, 3), ps.Point(80, 50, 3)])
    ], None)
                     )
    templates.append(Template("V", [
        ps.Point_cloud("V1", [ps.Point(30, 7, 1), ps.Point(40, 37, 1),
                              ps.Point(40, 37, 2), ps.Point(50, 7, 2)])
        ,
        ps.Point_cloud("V2", [ps.Point(0, 7, 1), ps.Point(25, 37, 1),
                              ps.Point(25, 37, 2), ps.Point(50, 7, 2)])
        ,
        ps.Point_cloud("V3", [ps.Point(30, 7, 1), ps.Point(40, 25, 1),
                              ps.Point(40, 25, 2), ps.Point(50, 7, 2)])
        ,
        ps.Point_cloud("V4", [ps.Point(30, 16, 1), ps.Point(33, 25, 1),
                              ps.Point(33, 25, 2), ps.Point(38, 7, 2)])
        ,
        ps.Point_cloud("V5", [ps.Point(30, 7, 1), ps.Point(33, 25, 1),
                              ps.Point(33, 25, 2), ps.Point(38, 16, 2)])
    ], None)
                     )
    templates.append(Template("D", [
        ps.Point_cloud("D1", [ps.Point(30, 7, 1), ps.Point(30, 67, 1),
                              ps.Point(30, 67, 2), ps.Point(50, 53, 2),
                              ps.Point(50, 53, 3), ps.Point(55, 37, 3),
                              ps.Point(55, 37, 4), ps.Point(50, 21, 4),
                              ps.Point(50, 21, 5), ps.Point(30, 7, 5)])
        ,
        ps.Point_cloud("D1", [ps.Point(30, 7, 1), ps.Point(30, 67, 1),
                              ps.Point(30, 67, 2), ps.Point(60, 53, 2),
                              ps.Point(60, 53, 3), ps.Point(65, 37, 3),
                              ps.Point(65, 37, 4), ps.Point(60, 21, 4),
                              ps.Point(60, 21, 5), ps.Point(30, 7, 5)])
        ,
    ], None)
                     )
    """templates.append(Template("RIGHT", [
        ps.Point_cloud("right1", [ps.Point(30, 47, 1), ps.Point(96, 7, 1)])
        ,
        ps.Point_cloud("right2", [ps.Point(30, 37, 1), ps.Point(96, 20, 1)])
        ], None)
    )
    templates.append(Template("LEFT", [
        ps.Point_cloud("left1", [ps.Point(30, 7, 1), ps.Point(96, 47, 1)])
        ,
        ps.Point_cloud("left2", [ps.Point(30, 20, 1), ps.Point(96, 37, 1)])
        ], None)
    )"""

    templates.append(Template("X", [
        ps.Point_cloud("X1", [ps.Point(30, 7, 1), ps.Point(60, 47, 1),
                              ps.Point(60, 7, 2), ps.Point(30, 47, 2)])
        ,
        ps.Point_cloud("X1_2", [ps.Point(30, 7, 1), ps.Point(60, 34, 1),
                                ps.Point(60, 7, 2), ps.Point(30, 34, 2)])
        ,
        ps.Point_cloud("X2", [ps.Point(30, 7, 1), ps.Point(60, 47, 1),
                              ps.Point(60, 7, 2), ps.Point(30, 47, 2),
                              ps.Point(30, 7, 3), ps.Point(60, 7, 3)])
        ,
        ps.Point_cloud("X3", [ps.Point(30, 7, 1), ps.Point(60, 47, 1),
                              ps.Point(60, 7, 2), ps.Point(30, 47, 2),
                              ps.Point(30, 47, 3), ps.Point(60, 47, 3)])
        ,
        ps.Point_cloud("X4", [ps.Point(30, 7, 1), ps.Point(60, 47, 1),
                              ps.Point(60, 7, 2), ps.Point(30, 47, 2),
                              ps.Point(30, 7, 3), ps.Point(30, 47, 3)])
    ], None)
                     )

    templates.append(Template("W", [
        ps.Point_cloud("W1", [ps.Point(30, 7, 1), ps.Point(40, 37, 1),
                              ps.Point(40, 37, 2), ps.Point(50, 7, 2),
                              ps.Point(50, 7, 3), ps.Point(60, 37, 3),
                              ps.Point(60, 37, 4), ps.Point(70, 7, 4)])
        ,
        ps.Point_cloud("W2", [ps.Point(30, 7, 1), ps.Point(50, 37, 1),
                              ps.Point(50, 37, 2), ps.Point(70, 7, 2),
                              ps.Point(70, 7, 3), ps.Point(90, 37, 3),
                              ps.Point(90, 37, 4), ps.Point(110, 7, 4)])
    ], None)
                     )

    templates.append(Template("L", [
        ps.Point_cloud("L1", [ps.Point(30, 27, 1), ps.Point(30, 37, 1),
                              ps.Point(30, 37, 2), ps.Point(40, 37, 2)])
        ,
        ps.Point_cloud("L2", [ps.Point(30, 17, 1), ps.Point(30, 37, 1),
                              ps.Point(30, 37, 2), ps.Point(40, 37, 2)])
    ], None)
                     )
    """templates.append(Template("M", [
        ps.Point_cloud("M1", [ps.Point(33, 45, 1), ps.Point(37, 7, 1),
                              ps.Point(37, 7, 2), ps.Point(50, 33, 2),
                              ps.Point(50, 33, 3), ps.Point(60, 13, 3),
                              ps.Point(60, 13, 4), ps.Point(67, 45, 4)])
        ,
        ps.Point_cloud("M2", [ps.Point(30, 45, 1), ps.Point(45, 7, 1),
                              ps.Point(45, 7, 2), ps.Point(65, 33, 2),
                              ps.Point(65, 33, 3), ps.Point(85, 7, 3),
                              ps.Point(85, 7, 4), ps.Point(100, 45, 4)])
        ,
        ps.Point_cloud("M3", [ps.Point(30, 57, 1), ps.Point(40, 7, 1),
                              ps.Point(40, 7, 2), ps.Point(47, 31, 2),
                              ps.Point(47, 31, 3), ps.Point(54, 7, 3),
                              ps.Point(54, 7, 4), ps.Point(64, 57, 4)])
    
        ], None)
    )"""

    templates.append(Template("Z", [
        ps.Point_cloud("Z1", [ps.Point(30, 7, 1), ps.Point(60, 7, 1),
                              ps.Point(60, 7, 2), ps.Point(30, 27, 2),
                              ps.Point(30, 27, 3), ps.Point(60, 27, 3)])
        ,
        ps.Point_cloud("Z2", [ps.Point(30, 7, 1), ps.Point(50, 12, 1),
                              ps.Point(50, 12, 2), ps.Point(30, 35, 2),
                              ps.Point(30, 35, 3), ps.Point(55, 30, 3)])
        ,
        ps.Point_cloud("Z3", [ps.Point(30, 7, 1), ps.Point(50, 12, 1),
                              ps.Point(50, 12, 2), ps.Point(20, 37, 2),
                              ps.Point(20, 37, 3), ps.Point(52, 33, 3)])
        ,
        ps.Point_cloud("Z4", [ps.Point(30, 21, 1), ps.Point(50, 8, 1),
                              ps.Point(50, 8, 2), ps.Point(23, 30, 2),
                              ps.Point(23, 30, 3), ps.Point(54, 27, 3)])
        ,
        ps.Point_cloud("Z5", [ps.Point(40, 7, 1), ps.Point(60, 7, 1),
                              ps.Point(60, 7, 2), ps.Point(30, 25, 2),
                              ps.Point(30, 25, 3), ps.Point(70, 27, 3)])
        ,
        ps.Point_cloud("Z6", [ps.Point(20, 7, 1), ps.Point(70, 7, 1),
                              ps.Point(70, 7, 2), ps.Point(30, 28, 2),
                              ps.Point(30, 28, 3), ps.Point(57, 27, 3)])
    ], None)
                     )

    return templates
