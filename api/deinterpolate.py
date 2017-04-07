# This provides a function, `deinterpolate()`, which takes coordinates for upper left hand and
#... bottom right hand corners, along with a series of points (x, y, value), and finds five
#... point values, namely the upper left, upper right, lower left, lower right and middle point

import math

VIEW_WIDTH = 100
VIEW_HEIGHT = 100

# This determines the maximum counted distance between an input point and desired output point
#... note that this is fairly arbitrary, and is roughly equivalent to gaussian blur radius
THRESHOLD = 2 * math.sqrt((VIEW_HEIGHT / 2)**2 + (VIEW_WIDTH / 2)**2)

# This determines how much wider the input dataset needs to be to fill the data requirements
INPUT_WIDTH = VIEW_WIDTH + 2 * THRESHOLD
INPUT_HEIGHT = VIEW_HEIGHT + 2 * THRESHOLD

# Simple point class
class Point(object):
	def __init__(self, x, y, val=None):
		self.x = x
		self.y = y
		self.val = val

	# def getPos(self):
	# 	return {"x": self.x, "y": self.y}

	# def getVal(self):
	# 	return self.val

	# def setVal(self, val):
	# 	self.val = val

def distance(relative_point, comparison_point):
	return math.sqrt((comparison_point.x-relative_point.x)**2 + (comparison_point.y-relative_point.y)**2)

def weight(val, dist):
	# TODO: Implement this function
	return val/dist 	# This is a BAD weighting system, it doesn't guarantee gradient matching

def calc_point(relative_point, points):

	for point in points:


def deinterpolate(points, upper_left, lower_right):
	result = {
		"upper_left":	Point(x = upper_left.x, y = upper_left.y)
		"upper_right":	Point(x = lower_right.x, y = upper_left.y)
		"lower_left":	Point(x = upper_left.x, y = lower_right.y)
		"lower_right":	Point(x = lower_right.x, y = lower_right.y)
		"center":		Point(x = (upper_left.x + lower_right.x) / 2.0,
			y = (upper_left.y + lower_right.y) / 2.0)
	}

