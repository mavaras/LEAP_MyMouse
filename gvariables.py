# -*- coding: utf-8 -*-

from win32api import GetSystemMetrics


class GVariables:
    def __init__(self):
        self.W = GetSystemMetrics(0)
        self.H = GetSystemMetrics(1)
        self.INF = 999999

        # scaled monitor dimensions for canvas
        self.window_width = W/2
        self.window_height = H/2

        # leap object
        self.listener = None

        # conf object
        self.configuration = None

        # gui
        self.main_window = None

        # PCRecognizer
        # pcr = None

        self.stdout = "__> program output\n"


W = GetSystemMetrics(0)
H = GetSystemMetrics(1)
"""LEAP_W = 320
LEAP_H = 200"""

INF = 999999

# scaled monitor dimensions for canvas
window_width = W/2
window_height = H/2
# canvas_width = 900
# canvas_height = 400

# leap object
listener = None

# conf object
configuration = None

# gui
main_window = None

# PCRecognizer
# pcr = None

stdout = "__> program output\n"
"""
# aux for canvas (used ?)
stroke_id = 0
points = []"""
