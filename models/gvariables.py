# -*- coding: utf-8 -*-

#from win32api import GetSystemMetrics
import os


class GVariables(object):

    def __init__(self):
        # screen dimensions
        screen_res = os.popen("xrandr  | grep \* | cut -d' ' -f4").read().split("x")

        '''self.W = GetSystemMetrics(0)
        self.H = GetSystemMetrics(1)'''
        self.W = int(screen_res[0])
        self.H = int(screen_res[1])

        self.INF = 999999

        # scaled monitor dimensions for canvas
        self.window_width = self.W/2
        self.window_height = self.H/2

        self.stdout = "__> program output\n"


gv = GVariables()
