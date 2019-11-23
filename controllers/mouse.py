# -*- coding: utf-8 -*-

# ===============MOUSE CLASS===============
# == used in leap_controller
# == performing mouse actions
# == stores mouse info


import time
import sys
if sys.platform == "win32":
    from controllers.Win32Handle import Win32Handle as OSHandler
elif sys.platform == "linux":
    from controllers.LinuxHandle import LinuxHandle as OSHandler


class Mouse:
    active = False
    left_clicked = False
    x, y = (0, 0)
    ydir = 1
    xdir = 1
    acc = 1
    vel = 1

    switch_mode = False
    switching = False
    swiping = False

    def __init__(self, x, y, dircx, dircy, acc, vel, active):
        self.x, self.y = x, y
        self.xdir = dircx  # -1 or 1 (left or right)
        self.ydir = dircy  # -1 or 1 (down or up)
        self.acc = acc
        self.vel = vel
        self.active = active  # mouse is being controlled by user

        self.left_clicked = False
        self.right_clicked = False
        self.left_pressed = False
        self.grabbing = False

        self.switch_mode = False  # if into switch mode (just hand position)
        self.switching = False  # if currently switching (switch mode + left or right switch)
        self.swipe = False  # if currently swiping (swipe mode + left or right swipe)
        self.last_swipe_time = time.time()

        self._OSHandler = OSHandler

    def lclick(self):
        """ performs a left click on the mouse"""
        self._OSHandler.lclick

    def rclick(self):
        """ performs a right click on the mouse"""
        self._OSHandler.rclick

    def vscroll(self, vel):
        """ performs a vertical scroll on the mouse

        :param vel: > 0 up, < 0 down
        """
        self._OSHandler.vscroll
