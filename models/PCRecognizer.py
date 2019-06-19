# -*- coding: utf-8 -*-

# ===============PCRecognizer ALGORITHM===============
# == functions
# == classes


# basic modules imports
import time

from template import init_templates
from PCRecognizer_functions import *
from gvariables import gv


class Result:
    def __init__(self, name, score, ms):
        self.name = name
        self.score = score
        self.ms = ms


num_points = 32  # points number to resample to


class PCRecognizer:

    def __init__(self):
        self.origin = ps.Point(gv.W / 4, gv.H / 4, -1)  # canvas point where to translate_to (canvas center)
        self.templates = init_templates()  # array storing all Template objects

    def normalize(self, points):
        """ this sets up points array received for proper algorithm application"""

        points = resample(points, 32)
        points = scale(points)
        points = translate_to(points, self.origin)
        return points

    def recognize(self, arr_points, print_all_matches=False):
        """ main PCRecognizer recognizing function. Starts all the process

        :param arr_points: array containing the points array of each finger if we are working with f1, its points array is into arr_points[0]
        :param print_all_matches: debugging purposes
        """

        t_ini = time.clock()

        # normalizing stroke(s)
        for c in range(len(arr_points)):  # if 1 finger len(arr_points) = 1
            arr_points[c] = self.normalize(arr_points[c])

        score = gv.INF
        template_n = -1
        found = False
        for c in range(len(self.templates)):
            print(c)
            if found:
                break

            if self.templates[c].fingers_point_cloud is None:
                # its a single stroke template (1 finger)
                n_nopes = 0
                for j in range(len(self.templates[c].point_cloud)):  # coincidence between points and all "subtemplates"
                    dist = greedy_cloud_match(arr_points[0], self.templates[c].point_cloud[j])  # normalizing template
                    if max((dist - 2.0) / -2.0, 0.0) == 0.0:
                        n_nopes += 1
                        if n_nopes == 3:
                            break

                    if print_all_matches:
                        coinc = "    similar to \"" + str(
                            self.templates[c].point_cloud[j].name + "\" about " + str(max((dist - 2.0) / -2.0, 0.0)))
                        print(coinc)

                    if dist < score:
                        score = dist
                        template_n = c
                        if max((dist - 2.0) / -2.0, 0.0) > 0.2:
                            found = True
                            break
            else:
                # its a complex stroke template (ALL fingers)
                pass

        t_fin = time.clock()
        if template_n == -1:
            return Result("no match", 0.0, t_fin - t_ini)

        else:
            return Result(self.templates[template_n].name,  # template matched
                          max((score - 2.0) / -2.0, 0.0),  # score achieved
                          t_fin - t_ini)  # time in ms
