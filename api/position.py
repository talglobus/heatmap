import math


class Point(object):						# Simple point class
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
	return math.sqrt((comparison_point.x-relative_point.x)**2
					 + (comparison_point.y-relative_point.y)**2)


# This is the bread and butter of position, determining the maximum distance from a given result
# point within which input points can affect its value (`threshold`), and the resulting space
# from within which input points need be accounted for. Note that `upper_left` and `lower_right`
# are the coordinates of the upper left and lower right hand corners of the viewport, while
# `threshold_upper_left` and `threshold_lower_right` are the coordinates of the upper left and
# lower right hand corners of the largest rectangle needed to cover all necessary input points.
# Because thresholding is based on circles, and these corners describe a rectangle larger than
# the necessary circles, there will be points within this rectangle that are not needed,
# but at least all necessary points will be accounted for within the threshold rectangle
def calc_needed(upper_left, lower_right):
	height = upper_left.y - lower_right.y
	width = lower_right.x - upper_left.x

	# This determines the maximum counted distance between an input point and desired output point
	# note that this is fairly arbitrary, and is roughly equivalent to gaussian blur radius
	threshold = 2 * math.sqrt((height / 2)**2 + (width / 2)**2)

	# This determines how much wider the input dataset needs to be to fill the data requirements
	threshold_upper_left = Point(x = upper_left.x - threshold, y = upper_left.y + threshold)
	threshold_lower_right = Point(x = lower_right.x + threshold, y = lower_right.y - threshold)

	return {
		"threshold": threshold,
		"threshold_upper_left": threshold_upper_left,
		"threshold_lower_right": threshold_lower_right
	}


# This is a simple function to evaluate if a point is within a box defined by `upper_left` and
# `lower_right` corners, for the purpose of quickly determining what points aren't needed
def in_box(point, upper_left, lower_right):
	if upper_left.x <= point.x <= lower_right.x and lower_right.y <= point.y <= upper_left.y:
		return True
	else:
		return False