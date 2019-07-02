# -*- coding: utf-8 -*-

from win32api import GetSystemMetrics


class GVariables(object):

    def __init__(self):
        # screen dimensions
        self.W = GetSystemMetrics(0)
        self.H = GetSystemMetrics(1)

        self.INF = 999999

        # scaled monitor dimensions for canvas
        self.window_width = self.W/2
        self.window_height = self.H/2

        self.stdout = "__> program output\n"


gv = GVariables()
