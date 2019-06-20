# -*- coding: utf-8 -*-

from win32api import GetSystemMetrics


class GVariables(object):
    def __init__(self):
        self.W = GetSystemMetrics(0)
        self.H = GetSystemMetrics(1)
        self.INF = 999999

        # scaled monitor dimensions for canvas
        self.window_width = self.W/2
        self.window_height = self.H/2

        # leap object
        self.listener = None

        # conf object
        self.configuration = None

        # gui
        self.main_window = None

        # PCRecognizer
        # pcr = None

        self.stdout = "__> program output\n"


gv = GVariables()
