# -*- coding: utf-8 -*-

W = 1920
H = 1080
"""LEAP_W = W/4.5
LEAP_H = H/4.5"""
LEAP_W = 320
LEAP_H = 200

INF = 999999


# scaled monitor dimensions for canvas
window_width = W/2
window_height = H/2
canvas_width = 900
canvas_height = 400


# leap object
listener = None

# conf object
configuration = None

# gui
main_window = None

# PCRecognizer
pcr = None

stdout = "__> programm output\n"

# aux for canvas (used ?)
stroke_id = 0
points = []
