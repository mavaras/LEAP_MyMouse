# -*- coding: utf-8 -*-

# ===============MAIN FILE===============
# == initializations
# ==== view
# ==== leap_controller
# ==== configuration
# ==== win32
# == threads


# basic modules imports
import time
import ctypes
import sys
import os
import math
import numpy as np
import threading

# aux modules imports
import win32api, win32con, win32gui
import cv2
import linecache2 as linecache
from collections import deque
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# self package imports
import gvariables

from models.configuration import *
from models.PCRecognizer import *

from views.gui_qtdesigner import *
import views.gui as gui

from controllers.leap_controller import *
from controllers.win32_functions import *
from controllers.aux_functions import *


# GLOBALS ?
#main_window = None
exit = False

# CLASS CONTAINING CONTROL POSSIBLE ACTIONS
class Actions():
	def show_desktop():
		pass
	def open_fexplorer():
		pass
	def minimizew():
		pass
	def maximizew():
		pass
	def closew():
		pass
	def open_app():
		pass
	def copy():
		pass
	def paste():
		pass
	def cut():
		pass
	

# various functions (ESTO NO DEBERÍA ESTAR AQUÍ)
# this function recognize one SINGLE stroke (if ALL fingers, one by one)
def recognize_stroke(points):
	print("recognizing stroke")
	aux = []
	aux.append(points)
	result = pcr.recognize(aux)
	
	return result

# this shows final score of current stroke (red label on canvas)
def print_score(result):
	score = "Result: matched with "+result.name+" about "+str(round(result.score, 2))
	main_window.label_score.setStyleSheet("color: red")
	main_window.label_score.setText(str(score))
	main_window.text_edit_2.append("\n"+str(score))

# handling gesture stroke match actions
def gesture_match(gesture_name):
	if gesture_name == "T":
		print("T gesture")
		if "-thread" in sys.argv:
			#handle = win32gui.FindWindow(None, r"Reproductor multimedia VLC")
			hwnd = get_current_window_hwnd()
			if gvariables.configuration.basic.closew == "T":
				close_window(hwnd)
			elif gvariables.configuration.basic.minimizew == "T":
				minimize_window(hwnd)
	
	elif gesture_name == "V":
		print("V gesture")
		if "-thread" in sys.argv:
			hwnd = get_current_window_hwnd()
			if gvariables.configuration.basic.closew == "V":
				close_window(hwnd)
			elif gvariables.configuration.basic.minimizew == "V":
				minimize_window(hwnd)

	elif gesture_name == "Z":
		print("Z gesture")
		if "-thread" in sys.argv:
			hwnd = get_current_window_hwnd()
			if gvariables.configuration.basic.closew == "Z":
				close_window(hwnd)
			elif gvariables.configuration.basic.minimizew == "Z":
				minimize_window(hwnd)
			
	elif gesture_name == "LEFT":
		print("LEFT gesture")
	elif gesture_name == "RIGHT":
		print("RIGHT gesture")
	print("")

# exits applications, closes all windows
def exit_app():
	print("exiting...")
	global exit
	exit = True
	main_window.close()
	cv2.destroyAllWindows()
	controller.remove_listener(listener)
	sys.exit()

def load_image(path):
	img = cv2.imread(path)
	data = np.array(bytearray(open(path, "rb").read()))
	#img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
	height, width, size = img.shape
	step = img.size / height
	qformat = QImage.Format_Indexed8

	if len(img.shape) == 3:
		if size == 4:
			qformat = QImage.Format_RGBA8888
		else:
			qformat = QImage.Format_RGB888

	img = QImage(img, width, height, step, qformat)
	img = img.rgbSwapped()

	return img, height, width


# thread which allows to make "G" + "G" by putting two hands on frame (python .py -thread)
# enables stroke gesture recognition (two hands on frame)
def thread_handler():
	print("thread_handler_init")
	import src.gvariables as gvariables
	global exit
	while not exit:
		if len(gvariables.listener.frame.hands) == 2 and not gvariables.listener.capture_frame:
			# here listener.frame_capture is False (we starting a new recording)
			time.sleep(.5)
			print("recording")
			while(gvariables.listener.hand_vel < 300):
				pass

			gvariables.listener.capture_frame = True

		elif len(gvariables.listener.frame.hands) == 1 and gvariables.listener.capture_frame:
			print("recording and recognizing captured")
			gvariables.listener.capture_frame = False                      # end of Leap capture
			pc = Point_cloud("f1", gvariables.listener.gesture[1])         # pc containing our new gesture
			pc.draw_on_canvas()                                 # drawing pc on canvas to see the shape

			global points, stroke_id
			points = gvariables.listener.gesture[1]                        # this allows "F" to work with mouse and hand stroke
			listener.c = 0

			result = recognize_stroke(points)
			gesture_match(result.name)
			gui.print_score(result)
			
			stroke_id = 0                                       # reseting values
			points = []
			gvariables.listener.clear_variables()

	print("thread_handler_end")


# MAIN BLOCK	
if __name__ == "__main__":
	# canvas variables
	points = gvariables.points                                  # where to store drawn points
	stroke_id = gvariables.stroke_id
	result = -1                                                 # result object
	pcr = PCRecognizer()                                        # algorithm class initialization

	# Leap setting up
	listener = leap_listener()
	controller = Leap.Controller()

	# listener initializer
	controller.add_listener(listener)

	# keeping Leap Motion working from background
	controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

	gvariables.listener = listener
	
	# Configuration
	gvariables.configuration = Conf()

	# GUI setting up
	app = QtGui.QApplication([])
	gvariables.main_window = gui.MainWindow()
	gvariables.main_window.initUI()
	gvariables.main_window.show()	
	
	# shell arguments
	for arg in sys.argv:
		if arg == "-thread":                                    # no keys gesture recognition enabled
			thread = threading.Thread(target=thread_handler)
			thread.setDaemon(True)
			thread.start()
		elif arg == "-allf":                                    # ALL fingers capture mode by default
			main_window.combo_box.setCurrentIndex(1)
		elif arg == "-scroll":                                  # scroll enabled
			gvariables.listener.vscrolling = True
			gvariables.listener.hscrolling = True
		elif arg == "-deepm":                                   # INTERACTION MODE: deep mode by default
			gvariables.listener.deep_mode = True
		elif arg == "-planem":                                  # INTERACTION MODE: plane mode by default
			gvariables.listener.plane_mode = True

	# win32 stuff
	opened_windows_names = []
	opened_windows_names = get_opened_windows_list()
	
	print("currently opened windows")
	print(opened_windows_names) #.encode("utf-8")
	#print("-> "+opened_windows_names[8])
	print(get_current_window_name())

	# drawing tests
	pcr.templates[5].point_cloud[0].draw_on_canvas(False)
	app.exec_()
