# -*- coding: utf-8 -*-

# ===============auxiliary functions===============
# == distances

import math


# sign of an int
sign = lambda a: (a>0) - (a<0)

# calculates the 3d distance between two given points
def distance_3d(x, y, z,
				x2, y2, z2):
	return math.sqrt(abs(x-x2) + abs(y-y2) + abs(z-z2))

# calculates distance between two given points
def distance(p1, p2):
	dx = p2.x - p1.x
	dy = p2.y - p1.y
	return math.sqrt(dx*dx + dy*dy)
