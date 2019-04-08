# -*- coding: utf-8 -*-

# ===============Template CLASS===============
# == Template class
# == load predefined templates


import points as ps


# TODO: add more templates


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
    templates.append(Template("RIGHT", [
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
    )

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
                              ps.Point(50, 7, 1), ps.Point(60, 37, 1),
                              ps.Point(60, 37, 2), ps.Point(70, 7, 2)])
        ], None)
    )

    return templates
