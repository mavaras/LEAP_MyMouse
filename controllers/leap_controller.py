# -*- coding: utf-8 -*-

# ===============LEAP API CONTROLLER===============
# == Leap interactions
# == frame representation
# == events
# == signals to view


# basic modules import
import sys
import numpy as np
import time

# aux modules imports
import cv2
from collections import deque
import win32api, win32con, win32gui
from pynput.keyboard import Key, Controller
from PyQt4.QtCore import QObject, pyqtSignal

# Leap Motion API
import lib.Leap as Leap

# self package imports
from aux_functions import *
from win32_functions import *
from gvariables import *


cv_frame_XY = np.zeros((H/2, W/3, 3), np.uint8)
cv_frame_XZ = np.zeros((H/2, W/3, 3), np.uint8)
	
# Class defining a single Point
class Point:
	def __init__(self, x, y, id):
		self.x = x
		self.y = y
		self.id = id
	
	# method to translate parent point to given location
	def convert_to(self, where_W, where_H):
		self.y = where_H - abs(self.y)   # Y invertion
		self.x = (W * self.x) / where_W
		self.y = (H * self.y) / where_H
		
# CLASS CONTAINING LEAP API
class leap_listener(Leap.Listener):
	frame = 0
	mouse = 0
	capture_frame = False

	# QObject class with those things to send to gui.py through signals
	class Leap_status(QObject):
		leap_connected = False
		sgn_leap_connected = pyqtSignal(bool)
		sgn_cv_frame_XY = pyqtSignal(np.ndarray)
		sgn_cv_frame_XZ = pyqtSignal(np.ndarray)
		
		def __init__(self):
			QObject.__init__(self)
			
		def emit_leap_connected(self, val):
			self.sgn_leap_connected.emit(val)
			
		def emit_cv_frame_XY(self, frame):
			self.sgn_cv_frame_XY.emit(frame)
		def emit_cv_frame_XZ(self, frame):
			self.sgn_cv_frame_XZ.emit(frame)
		

	# this class represents a mouse object for better handling
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
			self.xdir = dircx
			self.ydir = dircy
			self.acc = acc
			self.vel = vel
			self.active = active
			self.left_clicked = False
			self.right_clicked = False
			self.left_pressed = False
			self.switch_mode = False

		def click(self):  # ?
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.x, self.y, 0, 0)
			#time.sleep(.2)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.x, self.y, 0, 0)

	def clear_variables(self):
		self.gesture = [[]*5 for c in range(600)]
		self.c = 0
		self.tail_points = []
		for c in range(0, 5):
			aux = deque([], 18)
			self.tail_points.append(aux)
		
	def on_init(self, controller):
		self.cv_frame_XY = np.zeros((H/2, W/3, 3), np.uint8)  # XY frame
		self.cv_frame_XZ = np.zeros((H/2, W/3, 3), np.uint8)  # XZ frame
		
		self.frame = controller.frame()
		self.status = self.Leap_status()
		self.mouse = self.Mouse(0, 0, 1, 1, 1, 5, False)
		self.capture_frame = False
		self.vscrolling = False
		self.hscrolling = False
		self.plane_mode = False
		self.deep_mode = False

		# this all temporary variables, just for testing
		p = []
		lim_points = 600
		self.gesture = [[]*5 for c in range(lim_points)]
		self.c = 0                              # contador gesture points
		self.d01 = 0
		self.on_frame_c = 0                     # contador pitch average
		self.lim_points = 400
		self.hand_vel = 0
		self.fingers_pos = [[0,0,0] for c in range(5)]
		self.fingers_vel = [[-1] for c in range(5)]
		self.tail_points = []
		for c in range(0, 5):
			aux = deque([], 18)
			self.tail_points.append(aux)

		print("initialized")

	@property
	def leap_status(self):
		return self.status.leap_connected
	
	def on_connect(self, controller):
		print("conected")

		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

		self.status.leap_connected = True
		self.status.emit_leap_connected(True)
		
		time.sleep(.5)
		#gvariables.main_window.change_leap_status(True)  # label

	def on_focus_lost(self, controller):
		print("Unfocused")
		controller.add_listener(gvariables.listener)

	def on_disconnect(self, controller):
		print("disconnected")
		self.status.leap_connected = False
		self.status.emit_leap_connected(False)
		#gvariables.main_window.change_leap_status(False)

	def on_exit(self, controller):
		print("exited")

	def leap_to_screen(self, leap_x, leap_y):
		leap_y += 200
		# avoiding to invert X when nearing windows borders
		x = -LEAP_W/2 if int(leap_x) < -LEAP_W/2 else leap_x
		#y = 0 if int(leap_y) > LEAP_H else leap_y + 1300
		
		# y invertion
		y = leap_y - canvas_height
		y = y - abs(y)
		
		x = x + LEAP_W/2
		x = abs((W * x) / (W/7.5))
		y = abs((H * y) / (H/4.5))
		
		#print("L"+str((leap_x,leap_y)))
		#print((x,y))
		return abs(x), abs(y)
		
	def on_frame(self, controller):
		self.frame = controller.frame()
		frame = self.frame

		# opencv canvas
		cv_frame_loc_XY = np.zeros((H/2, W/3, 3), np.uint8)  # XY frame
		cv_frame_loc_XZ = np.zeros((H/2, W/3, 3), np.uint8)  # XZ frame

		if len(frame.hands) == 2:
			# two hands if frame
			cv2.putText(cv_frame_loc_XY, "Two hands in frame",
					   (190, H/2 - 50), cv2.FONT_HERSHEY_SIMPLEX,
						0.8, (255,255,255), 1, cv2.LINE_AA)
			cv2.circle(cv_frame_loc_XY, (H/4 + 50, W/6 - 50), 100, [255, 0, 0], 1)
			cv2.putText(cv_frame_loc_XZ, "Two hands in frame",
					   (190, H/2 - 50), cv2.FONT_HERSHEY_SIMPLEX,
						0.8, (255,255,255), 1, cv2.LINE_AA)
			cv2.circle(cv_frame_loc_XZ, (H/4 + 50, W/6 - 50), 100, [255, 0, 0], 1)
			
		for hand in frame.hands:
			if hand.is_right:
				cv2.putText(cv_frame_loc_XY, "X to Y representation (vertical plane)",
						   (50, H/2 - 50), cv2.FONT_HERSHEY_SIMPLEX,
							0.8, (255,255,255), 1, cv2.LINE_AA)
				cv2.putText(cv_frame_loc_XZ, "X to Z representation (horizontal plane)",
						   (50, H/2 - 50), cv2.FONT_HERSHEY_SIMPLEX,
							0.8, (255,255,255), 1, cv2.LINE_AA)
				
				#elif len(frame.hands) == 1:
				self.hand_vel = max(abs(hand.palm_velocity[0]),
									abs(hand.palm_velocity[1]),
									abs(hand.palm_velocity[2]))
				
				# one hand into frame
				if self.mouse.active == True:
					if self.vscrolling:
						# scrolling
						# angle between Z and Y (X rotations)
						pitch = hand.direction.pitch * Leap.RAD_TO_DEG
						if pitch < -13:
							print("vscroll down")
							cx, cy = win32api.GetCursorPos()
							vel = -int(40-((90-abs(pitch))/3))
							win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, cx, cy, vel, 0)

						elif pitch > 36:
							print("vscroll up")
							cx, cy = win32api.GetCursorPos()
							vel = int(30-((90-pitch)/3))
							win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, cx, cy, vel, 0)

						# horizontal scroll ??
						# angle between Z and X (Y rotations)
						roll = hand.direction.roll * Leap.RAD_TO_DEG
						keyboard = Controller()
						if roll < -50:
							"""print("hscroll down")
							keyboard.press(Key.ctrl)
							keyboard.press("s")"""
							
						elif roll > 50:
							"""print("hscroll up")
							cx, cy = win32api.GetCursorPos()
							vel = int(30-((90-pitch)/3))
							win32api.mouse_event(win32con.EVENTF_WHEEL, cx, cy, vel, 0)"""
							
					# INTERACTION modes
					if self.deep_mode:
						finger1 = hand.fingers[1]
						f1_pos = finger1.tip_position
						"""print(f1_pos.z)

						x, y = self.leap_to_screen(f1_pos.x, f1_pos.y)

						# mouse movement:
						self.mouse.xdir = 1 if x > W/2 else -1
						self.mouse.ydir = 1 if abs(y) < H/2 else -1
						win32api.SetCursorPos((int(abs(x)+self.mouse.xdir),
											   int(abs(y))+self.mouse.ydir))
						self.mouse.x, self.mouse.y = int(abs(x)), int(abs(y))"""
						
					elif self.plane_mode:
						f1 = hand.fingers[0]
						f2 = hand.fingers[1]
						f3 = hand.fingers[2]
						dist_0_1 = distance(Point(f1.tip_position.x,f1.tip_position.z,-1),
											Point(f2.tip_position.x,f2.tip_position.z,-1))   # this works better on XZ plane
						dist_1_2 = distance_3d(f3.tip_position.x,f3.tip_position.y,f3.tip_position.z,
											   f2.tip_position.x,f2.tip_position.y,f2.tip_position.z)
						
						# ________SWITCH windows________
						# angle between X and Y (Z rotations)
						roll = abs(hand.palm_normal.roll * Leap.RAD_TO_DEG)
						yaw = hand.direction.yaw * Leap.RAD_TO_DEG
						if roll > 50:
							 # we are into switch mode
							self.mouse.switch_mode = True
							direction = int(yaw/abs(yaw))
							if hand.palm_velocity.x > 150 and not self.mouse.switching:
								# utf-8 esta jodiendo por ejemplo en (u)Torrent

								self.mouse.switching = True
								#print("direction: "+str(direction))
								aux = get_current_window_name()
								curr_window_index = opened_windows_names.index(aux)
								if direction == 1:
									print("right SWIPE")
									if curr_window_index == len(opened_windows_names) - 1:
										curr_window_index = 0
									name = opened_windows_names[curr_window_index+1]
								else:
									print("left SWIPE")
									if curr_window_index == 1:  # always Start it's the first one in list(0) (Windows only?)
										curr_window_index = len(opened_windows_names)-1
									name = opened_windows_names[curr_window_index-1]

								bring_window_to_top(win32gui.FindWindow(None, name))
								time.sleep(.5)
							else:
								self.mouse.switching = False

						else:
							self.mouse.switch_mode = False
							self.mouse.switching = False
							
							# ________LCLICK________
							# for keep performance when hand pitch (X rotations) >>
							pitch = hand.direction.pitch * Leap.RAD_TO_DEG
							if dist_0_1 < 80 - 15*abs(pitch)//35:
								if not self.mouse.left_clicked and not self.mouse.left_pressed:
									print("click")
									self.mouse.left_clicked = True
									cx, cy = win32api.GetCursorPos()
									win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, cx, cy, 0, 0)
									time.sleep(.2)
									win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, cx, cy, 0, 0)
							else:
								self.d01 = dist_0_1
								if self.mouse.left_clicked:
									print("released")
									self.mouse.left_clicked = False

							# ________GRABB________
							#print(dist_1_2)
							if dist_1_2 < 5.8:
								if not self.mouse.left_clicked and not self.mouse.left_pressed:
									print("grabbed")
									cx, cy = win32api.GetCursorPos()
									win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, cx, cy, 0, 0)
									self.mouse.left_pressed = True
							else:
								if self.mouse.left_pressed:
									print("ungrabbed")
									cx, cy = win32api.GetCursorPos()
									#time.sleep(.2)
									win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, cx, cy, 0, 0)
									self.mouse.left_pressed = False

							# ________RCLICK________
							if f3.tip_velocity.y < -90 and abs(f2.tip_velocity.y) < 30 and not self.mouse.right_clicked:
								print("rclick")
								self.mouse.right_clicked = True
								#print(str(f3.tip_velocity.y)+" _ "+str(f2.tip_velocity.y))
								cx, cy = win32api.GetCursorPos()
								win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, cx, cy, 0, 0)
								time.sleep(.2)
								win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, cx, cy, 0, 0)
							else:
								if self.mouse.right_clicked:
									self.mouse.right_clicked = False


				for finger in hand.fingers:
					self.fingers_vel[finger.type] = max(abs(finger.tip_velocity.x), abs(finger.tip_velocity.y), abs(finger.tip_velocity.z))
					fx, fy, fz = finger.tip_position.x, finger.tip_position.y, finger.tip_position.z
					sx, sy = self.leap_to_screen(fx, fy)
					if distance(Point(sx, sy, -1), Point(self.fingers_pos[finger.type][0],
														 self.fingers_pos[finger.type][1], -1)) > 3:
						self.fingers_pos[finger.type] = (sx, sy, fz)

					# drawing things
					cv2.circle(cv_frame_loc_XY, (int(fx) + 250, int(H/2 - abs(fy))), 11, [255, 255, 255], 1)
					if finger.type != 0:
						cv2.line(cv_frame_loc_XY,
								 (int(fx) + 250, int(H/2 - abs(fy))),
								 (int(hand.fingers[finger.type-1].tip_position.x) + 250,
								  int(H/2 - abs(hand.fingers[finger.type-1].tip_position.y))
								 ),
								 (255, 255, 255), 1)
						cv2.line(cv_frame_loc_XZ,
								 (int(fx) + 250, int(sign(fz)*fz) + 220),
								 (int(hand.fingers[finger.type-1].tip_position.x) + 250,
								  int(220 + abs(hand.fingers[finger.type-1].tip_position.z))
								 ),
								 (255, 255, 255), 1)

					self.tail_points[finger.type].append((int(fx) + 250, int(H/2 - abs(fy)), 220 + sign(fz)*int(abs(fz))))
					for point in self.tail_points[finger.type]:
						cv2.circle(cv_frame_loc_XY, (point[0], point[1]), 6, [205, 205, 205], 1)
						cv2.circle(cv_frame_loc_XZ, (point[0], point[2]), 6, [205, 205, 205], 1)

					if len(self.tail_points) == 10:
						self.tail_points[finger.type].popleft()

					# recording coordinates
					if self.capture_frame:
						#print(str(finger.type)+" "+str(finger.tip_position))
						self.gesture[finger.type].append(Point(fx, fy, -1))
						self.gesture[finger.type][len(self.gesture[finger.type])-1].convert_to(W/2, H/2)
						#self.c += 1

					# cursor movement
					if len(frame.hands) == 1 and finger.type == gvariables.configuration.basic.mm and self.mouse.active and not self.mouse.switch_mode:
						# cursor movement
						self.mouse.xdir = 1 if sx > W/2 else -1
						self.mouse.ydir = 1 if abs(sy) < H/2 else -1
						
						"""print(sx)
						print(sy)
						print("")"""
						
						win32api.SetCursorPos((
							int(abs(self.fingers_pos[gvariables.configuration.basic.mm][0])),  # x
							int(abs(self.fingers_pos[gvariables.configuration.basic.mm][1]))   # y
						))
						
						self.mouse.x = int(abs(self.fingers_pos[gvariables.configuration.basic.mm][0]))
						self.mouse.y = int(abs(self.fingers_pos[gvariables.configuration.basic.mm][1]))

					"""if finger.type == 1 and self.mouse.active == True:
						# avoiding to invert X and Y when nearing windows borders
						x = -LEAP_W/2 if int(finger.tip_position.x) < -LEAP_W/2 else finger.tip_position.x
						# y invertion
						y = finger.tip_position.y - canvas_height
						y = y - abs(y)

						x = x + LEAP_W/2
						x = (W * x) / LEAP_W
						y = (H * y) / LEAP_H
						y += 1500

						self.mouse.xdir = 1 if x > W/2 else -1
						self.mouse.ydir = 1 if abs(y) < H/2 else -1

						win32api.SetCursorPos((int(abs(x)+self.mouse.vel*self.mouse.xdir),
											   int(abs(y))+self.mouse.vel*self.mouse.ydir))
						self.mouse.x, self.mouse.y = int(abs(x)), int(abs(y))"""

					self.on_frame_c += 1

		#global cv_frame_XY, cv_frame_XZ
		self.cv_frame_XY = cv_frame_loc_XY
		self.cv_frame_XZ = cv_frame_loc_XZ
		self.status.emit_cv_frame_XY(self.cv_frame_XY)
		self.status.emit_cv_frame_XZ(self.cv_frame_XZ)
		#cv2.imshow(cv2_window_name, cv_frame_XY)
		key = cv2.waitKey(5) & 0xFF
		if key == ord("q"):
			exit_app()
