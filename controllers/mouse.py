# -*- coding: utf-8 -*-

# ===============MOUSE CLASS===============
# == used in leap_controller
# == pushing mouse buttons
# == storing mouse info


import time
import win32api, win32con, win32gui


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

	def __init__(self, x, y, dircx, dircy, acc, vel, active):
		self.x, self.y = x, y
		self.xdir = dircx					# -1 or 1 (left or right)
		self.ydir = dircy					# -1 or 1 (down or up)
		self.acc = acc
		self.vel = vel
		self.active = active			# mouse is being controlled by user

		self.left_clicked = False
		self.right_clicked = False
		self.left_pressed = False
		
		self.switch_mode = False  # if into switch mode (just hand position)
		self.switching = False		# if currently switching (switch mode + left or right swipe)

	def lclick(self):
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.x, self.y, 0, 0)
		time.sleep(.2)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.x, self.y, 0, 0)

	def rclick(self):
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.x, self.y, 0, 0)
		time.sleep(.2)
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.x, self.y, 0, 0)

	def vscroll(self, vel):
		win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, self.x, self.y, vel, 0)
