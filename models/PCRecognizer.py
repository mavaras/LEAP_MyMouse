# -*- coding: utf-8 -*-

# ===============PCRecognizer ALGORITHM===============
# == functions
# == classes


# basic modules imports
import time
import sys

# aux modules imports
from PyQt4.QtGui import *
from PyQt4 import QtCore  # ?

# self package imports
from gvariables import *
import gvariables
from controllers.aux_functions import *


# ===============PCRecognizer algorithm things (functions + classes)===============

def greedy_cloud_match(points, pc):
	""" match two point_cloud by calculating distance between their points
	between our points and the template
	"""
	
	e = 0.50
	step = math.floor(math.pow(len(points), 1.0 - e))
	minimum = INF
	for c in range(0, len(points)):
		d1 = cloud_distance(points, pc.points, c)
		d2 = cloud_distance(pc.points, points, c)
		minimum = min(minimum, min(d1, d2))
		c += step

	return minimum

def cloud_distance(pc1, pc2, start):
	""" this function returns the geometric distance between two provided point_clouds"""
	
	aux = [False] * len(pc1)    # empty auxiliar array
	suma = 0
	w = start
	while True: # something like a do while?
		index = -1
		minimum = INF
		for j in range(0, len(aux)):
			if False == aux[j]:
				dist = distance(pc1[w], pc2[j])
				#print("d: "+str(minimum))
				if dist < minimum:
					minimum = dist
					index = j

		aux[index] = True
		# this float parsing is neccesary for this python 2.x
		weigth = 1 - (float((w - start + len(pc1) % len(pc1))) / float(len(pc1)))
		suma += weigth * minimum
		w = (w + 1) % len(pc1)

		if w == start:
			break

	return suma

def resample(points, resample_len):
	"""resamples provided point_cloud in order to set homogenous lengths for properly comparaison
	resample_length indicates the length which to resample the pc.
	"""
	
	interval = path_length(points) / (resample_len - 1)
	d = 0.0
	new_points = []
	new_points.append(points[0])
	c = 1
	for p in points:
		try:
			if points[c].id == points[c - 1].id:                 # we are int he same stroke
				dist = distance(points[c - 1], points[c])
				if d + dist >= interval:
					px = points[c-1].x + ((interval - d)/dist) * (points[c].x - points[c-1].x)
					py = points[c-1].y + ((interval - d)/dist) * (points[c].y - points[c-1].y)
					p = Point(px, py, points[c].id)
					new_points.append(p)
					points.insert(c, p)                          # insert p in c position, reasigning all elements
					d = 0.0

				else:
					d += dist
			c += 1
			
		except:
			break

	if len(new_points) == resample_len - 1:
		new_points.append(Point(points[len(points) - 1].x,
								points[len(points) - 1].y,
								points[len(points) - 1].id))

	return new_points

def scale(points):
	""" this funciton returns the same point_cloud in different scales in order to comparaison"""
	
	min_x = INF
	min_y = INF
	max_x = -INF
	max_y = -INF
	for c in range(len(points)):
		min_x = min(min_x, points[c].x)
		min_y = min(min_y, points[c].y)
		max_x = max(max_x, points[c].x)
		max_y = max(max_y, points[c].y)

	scale = max(max_x - min_x, max_y - min_y)
	new_points = []
	for c in range(len(points)):
		px = (points[c].x - min_x) / scale
		py = (points[c].y - min_y) / scale
		new_points.append(Point(px, py, points[c].id))

	return new_points

def translate_to(points, where):
	""" translates given points set (point_cloud) to provided centroid. It maps all pc to origin,
	in order to recognize pc that are similar but in different coordinates
	"""
	
	centroid = get_centroid(points)
	new_points = []
	for c in range(0, len(points)):
		px = points[c].x + where.x - centroid.x
		py = points[c].y + where.y - centroid.y
		new_points.append(Point(px, py, points[c].id))

	return new_points

def amplify(points, mult):
	""" amplifies given collection of points keeping its distances between each other attending 
	to mult argument
	"""
	
	new_points = []
	x = points[0].x
	y = points[0].y
	new_points.append(Point(x, y, points[0].id))
	for c in range(1, len(points)):
		x += mult*(points[c].x - points[c - 1].x)
		y += mult*(points[c].y - points[c - 1].y)
		new_points.append(Point(x, y, points[c].id))

	return new_points

def get_centroid(points):
	""" this function calculates given points_cloud's centroid"""
	
	x = 0.0
	y = 0.0
	for c in range(0, len(points)):
		x += points[c].x
		y += points[c].y

	x /= len(points)
	y /= len(points)

	return Point(x, y, 0)

def path_length(points):
	""" calculates the length of a single point into a point_cloud"""
	
	dist = 0.0
	for c in range(1, len(points)):
		if points[c].id == points[c - 1].id:
			dist += distance(points[c - 1], points[c])

	return dist

def init_templates():
	""" initialize templates array for PCRecognizer class"""
	
	templates = []  
	# single stroke templates (all fingers doing the same if various fingers) (1 finger)
	templates.append(Template("T", [
		# Template point clouds
		# different ways of drawing Template.name (T) for better recognition
		Point_cloud("T1", [Point(30, 7, 1), Point(103, 7, 1),
						   Point(66, 7, 2), Point(66, 87, 2)])
		,
		Point_cloud("T2", [Point(30, 7, 1), Point(123, 7, 1),
						   Point(80, 17, 2),Point(30, 7, 2),
						   Point(80, 17, 3),Point(80, 77, 3)])
		,
		Point_cloud("T3", [Point(30, 7, 1), Point(123, 7, 1),
						   Point(80, 17, 2),Point(30, 7, 2),
						   Point(80, 17, 3),Point(80, 50, 3)])
		], None)
	)
	templates.append(Template("V", [
		Point_cloud("V1", [Point(30, 7, 1), Point(40, 37, 1),
						   Point(40, 37, 2),Point(50, 7, 2)])
		,
		Point_cloud("V2", [Point(0, 7, 1), Point(25, 37, 1),
						   Point(25, 37, 2),Point(50, 7, 2)])
		,
		Point_cloud("V3", [Point(30, 7, 1), Point(40, 25, 1),
						   Point(40, 25, 2),Point(50, 7, 2)])
		,
		Point_cloud("V4", [Point(30, 16, 1), Point(33, 25, 1),
						   Point(33, 25, 2),Point(38, 7, 2)])
		,
		Point_cloud("V5", [Point(30, 7, 1), Point(33, 25, 1),
						   Point(33, 25, 2),Point(38, 16, 2)])
		], None)
	)
	templates.append(Template("RIGHT", [
		Point_cloud("right1", [Point(30, 47, 1), Point(96, 7, 1)])
		,
		Point_cloud("right2", [Point(30, 37, 1), Point(96, 20, 1)])
		], None)
	)
	templates.append(Template("LEFT", [
		Point_cloud("left1", [Point(30, 7, 1), Point(96, 47, 1)])
		,
		Point_cloud("left2", [Point(30, 20, 1), Point(96, 37, 1)])
		], None)
	)
	"""templates.append(Template("X", [
		Point_cloud("X1", [Point(30, 7, 1), #Point(45, 20, 1),
						   Point(60, 47, 1),
						   Point(60, 7, 2), Point(30, 47, 2)])
		], None)
	)"""
	templates.append(Template("X", [
		Point_cloud("X1", [Point(30, 7, 1), Point(60, 47, 1),
						   Point(60, 7, 2), Point(30, 47, 2)])
		,
		Point_cloud("X1_2", [Point(30, 7, 1), Point(60, 34, 1),
							 Point(60, 7, 2), Point(30, 34, 2)])
		,
		Point_cloud("X2", [Point(30, 7, 1), Point(60, 47, 1),
						   Point(60, 7, 2), Point(30, 47, 2),
						   Point(30, 7, 3), Point(60, 7, 3)])
		,
		Point_cloud("X3", [Point(30, 7, 1), Point(60, 47, 1),
						   Point(60, 7, 2), Point(30, 47, 2),
						   Point(30, 47, 3),Point(60, 47, 3)])
		,
		Point_cloud("X4", [Point(30, 7, 1), Point(60, 47, 1),
						   Point(60, 7, 2), Point(30, 47, 2),
						   Point(30, 7, 3), Point(30, 47, 3)])
		], None)
	)
	templates.append(Template("W", [
		Point_cloud("W1", [Point(30, 7, 1), Point(40, 37, 1),
						   Point(40, 37, 2),Point(50, 7, 2),
						   Point(50, 7, 1), Point(60, 37, 1),
						   Point(60, 37, 2),Point(70, 7, 2)])
		], None)
	)
	
	# complex stroke templates (each finger analized individually) (ALL fingers)    
	
	return templates


# CLASS DEFINITIONS
# this CLASS represents one single point
# convert_to method does the translation between Leap coordinates to canvas or something ones
class Point:
	def __init__(self, x, y, id):
		self.x = x
		self.y = y
		self.id = id

	def convert_to(self, where_W, where_H):
		self.y = where_H - abs(self.y)   # Y invertion
		self.x = (W * self.x) / where_W
		self.y = (H * self.y) / where_H

	def draw_on_canvasTK(self, radius):
		canvas.create_oval(self.x-radius, self.y-radius,
						   self.x+radius, self.y+radius, fill = "#aaaaaa")

	def draw_on_canvas(self, radius, path):
		eval("gvariables.main_window.widget_canvas."+path+
			 ".addEllipse(QtCore.QRectF(self.x, self.y, radius, radius))")
		gvariables.main_window.widget_canvas.update()
		

# point cloud = collection of points defining a shape, it's like a points array
class Point_cloud:
	def __init__(self, name, points, where_to_translate=Point(W/4, H/4, -1)):
		self.origin = where_to_translate
		self.name = name
		self.points = resample(points, 32)                       # point cloud resizing
		self.points = scale(self.points)                         # point cloud scaling
		self.points = translate_to(self.points, self.origin)     # point cloud centering

	def draw_on_canvas(self, flag=True):
		aux_points = []                                          # to not overwritting original self.points array
		aux_points = amplify(self.points, 200)                   # kind of scale reversion
		aux_points = translate_to(aux_points, Point(self.origin.x, self.origin.y/2, -1))  # translating amplilfied pc to center
		dic = {"f0":"path_points_0", "f1":"path_points_1",
			   "f2":"path_points_2", "f3":"path_points_3", "f4":"path_points_4"}

		#aux_points = points
		c = 0
		if flag:
			path = dic.get(self.name)
		else:                                                    # black color by default
			path = "path_points_1"
		
		for p in aux_points:
			if c == num_points:
				# last point
				p.draw_on_canvas(10, path)
			else:
				p.draw_on_canvas(6, path)
				
			c += 1

# this CLASS represents a full Template, that's it a template representing a form (name)
# but with some different ways of representing it (point_cloud array)
class Template:
	def __init__(self, name, point_cloud, fingers_point_cloud):
		self.name = name
		self.point_cloud = point_cloud
		self.fingers_point_cloud = fingers_point_cloud           # this if template is a complex one

# this CLASS stores the final result of the algorithm, containing the match
class Result:
	def __init__(self, name, score, ms):
		self.name = name
		self.score = score
		self.ms = ms


# MAIN ALGORITHM CLASS
# contains all the templates and starts all the process
num_points = 32                                                  # points number to resample to
origin = Point(W/4, H/4, -1)                                     # canvas point where to translate_to (canvas center)
class PCRecognizer:
	templates = init_templates()                                 # array storing all Template objects

	def normalize(self, points):
		""" this sets up points array received for proper algorithm application"""
		
		points = resample(points, 32)
		points = scale(points)
		points = translate_to(points, origin)
		return points

	def recognize(self, arr_points, print_all_matches = False):
		"""	arr_points = array containing the points array of each finger
		if we are working with f1, its points array is into arr_points[0]
		"""
		
		t_ini = time.clock()

		# normalizing stroke(s)  
		for c in range(0, len(arr_points)):                      # (if 1 finger len(arr_points) = 1
			arr_points[c] = self.normalize(arr_points[0])

		score = INF
		template_n = -1
		for c in range(0, len(self.templates)):
			if self.templates[c].fingers_point_cloud == None:
				# its a single stroke template (1 finger)
				for j in range(0, len(self.templates[c].point_cloud)):
					# normalizing template
					dist = greedy_cloud_match(arr_points[0], self.templates[c].point_cloud[j])
					# coincidence between points and all "subtemplates"
					if print_all_matches:
						coinc = "    similar to \""+str(self.templates[c].point_cloud[j].name+"\" about "+str(max((dist - 2.0) / -2.0, 0.0)))
						print(coinc)
						#main_window.text_edit_2.append(coinc)
					if dist < score:
						score = dist
						template_n = c
			else:
				# its a complex stroke template (ALL fingers)
				pass

		t_fin = time.clock()
		if template_n == -1:
			return Result("no match", 0.0, t_fin - t_ini)

		else:
			# process is finished, we return the result
			print("score: "+str(score))
			return Result(self.templates[template_n].name,      # template matched
						  max((score - 2.0) / -2.0, 0.0),       # score achieved
						  t_fin - t_ini)                        # time in ms
