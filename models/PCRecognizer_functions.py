# -*- coding: utf-8 -*-

import math
import points as ps
from gvariables import *
from controllers.aux_functions import distance

num_points = 32


def greedy_cloud_match(points, pc):
    """ match two point_cloud by calculating distance between their points
    between our points and the template

    :param points: points array (frequently user stroke)
    :param pc: point cloud which to match to (template)
    """
    e = 0.50
    step = math.floor(math.pow(len(points), 1.0 - e))
    minimum = INF
    for c in range(0, len(points)):
        d1 = cloud_distance(points, pc.points, c)
        d2 = cloud_distance(pc.points, points, c)
        minimum = min(minimum, min(d1, d2))
        c += step

    return minimum


def cloud_distance(pc1, pc2, start):
    """ this function returns the geometric distance between two provided point_clouds

    :param pc1: point cloud 1
    :param pc2: point cloud 2
    :param start: start point
    :return: distance
    """

    aux = [False] * len(pc1)  # auxiliary array
    suma = 0
    w = start
    while True:
        index = -1
        minimum = INF
        for j in range(0, len(aux)):
            if not aux[j]:
                dist = distance(pc1[w], pc2[j])
                if dist < minimum:
                    minimum = dist
                    index = j

        aux[index] = True

        # this float parsing is necessary for this python 2.x
        weight = 1 - (float((w - start + len(pc1) % len(pc1))) / float(len(pc1)))
        suma += weight * minimum
        w = (w + 1) % len(pc1)

        if w == start:
            break

    return suma


def resample(points, resample_len):
    """resamples provided point_cloud in order to set homogeneous lengths for properly comparison
    resample_length indicates the length which to resample the pc.

    :param points: points point_cloud
    :param resample_len: usually 32
    :return: points
    """

    interval = path_length(points) / (resample_len - 1)
    d = 0.0
    new_points = [points[0]]
    c = 1
    for p in points:
        try:
            if points[c].id == points[c - 1].id:  # we are int he same stroke
                dist = distance(points[c - 1], points[c])
                if d + dist >= interval:
                    px = points[c - 1].x + ((interval - d) / dist) * (points[c].x - points[c - 1].x)
                    py = points[c - 1].y + ((interval - d) / dist) * (points[c].y - points[c - 1].y)
                    p = ps.Point(px, py, points[c].id)
                    new_points.append(p)
                    points.insert(c, p)  # insert p in c position, reassigning all elements
                    d = 0.0

                else:
                    d += dist
            c += 1

        except:
            break

    if len(new_points) == resample_len - 1:
        new_points.append(ps.Point(points[len(points) - 1].x,
                                   points[len(points) - 1].y,
                                   points[len(points) - 1].id))

    return new_points


def scale(points):
    """ this function returns the same point_cloud in different scales in order to comparison

    :param points: points
    :return: points"""

    min_x = INF
    min_y = INF
    max_x = -INF
    max_y = -INF
    for c in range(len(points)):
        min_x = min(min_x, points[c].x)
        min_y = min(min_y, points[c].y)
        max_x = max(max_x, points[c].x)
        max_y = max(max_y, points[c].y)

    scale = max(max_x - min_x, max_y - min_y)
    scale = 1 if scale == 0 else scale
    new_points = []
    for c in range(len(points)):
        px = (points[c].x - min_x) / scale
        py = (points[c].y - min_y) / scale
        new_points.append(ps.Point(px, py, points[c].id))

    return new_points


def translate_to(points, where):
    """ translates given points set (point_cloud) to provided centroid. It maps all pc to origin,
    in order to recognize pc that are similar but in different coordinates

    :param points: points
    :param where: Point where to translate points
    :return: translated points
    """

    centroid = get_centroid(points)
    new_points = []
    for c in range(0, len(points)):
        px = points[c].x + where.x - centroid.x
        py = points[c].y + where.y - centroid.y
        new_points.append(ps.Point(px, py, points[c].id))

    return new_points


def amplify(points, mult):
    """ amplifies given collection of points keeping its distances between each other attending
    to mult argument

    :param points: points
    :param mult: amplifying size
    :return: points
    """

    new_points = []
    x = points[0].x
    y = points[0].y
    new_points.append(ps.Point(x, y, points[0].id))
    for c in range(1, len(points)):
        x += mult * (points[c].x - points[c - 1].x)
        y += mult * (points[c].y - points[c - 1].y)
        new_points.append(ps.Point(x, y, points[c].id))

    return new_points


def get_centroid(points):
    """ this function calculates given points_cloud's centroid

    :param points: points
    :return: Point
    """

    x = 0.0
    y = 0.0
    for c in range(0, len(points)):
        x += points[c].x
        y += points[c].y

    x /= len(points)
    y /= len(points)

    return ps.Point(x, y, 0)


def path_length(points):
    """ calculates the length of a stroke defined by points
    sum of each stroke_id length

    :param points: points
    :return: length
    """

    dist = 0.0
    for c in range(1, len(points)):
        if points[c].id == points[c - 1].id:
            dist += distance(points[c - 1], points[c])

    return dist
