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
	return math.sqrt((comparison_point.x-relative_point.x)**2
		+ (comparison_point.y-relative_point.y)**2)

# This function is the bread and butter of this module, determining how, given a point's value
#... and the distance from it to the result point, it is weighted into the value assigned to the
#... result. There are a few rules that need to be followed for this to be a good weighting:
# 1) If all input values are the same, all result values anywhere in the range should match
#	 - This means that if the input points all have the value 5, all result points should be 5
#		regardless of where they are in relation to the input points
# 2) Result values shouldn't be biased up or down because they happen to not be near input points
#	 - This means that overall weighting should average to some constant at all points, like
#		how at any point in the unit circle, sin^2(theta) + cos^2(theta) is ALWAYS 1
# 3) The closer a result point to an input point, the greater weight the input point should have
#	on the result point. This just means that closer weights are weighted above farther points
def weight(val, dist):
	# TODO: Implement this function
	return val * (THRESHOLD - dist) / THRESHOLD
	# return val/dist 	# This is a BAD weighting system, it doesn't guarantee gradient matching

def calc_point(relative_point, points):
	cumulative_sum = 0

	# This list comprehension produces tuples of points and distances (to prevent recalculation
	#... of distance) for all points within `THRESHOLD` distance
	in_range = [(point, distance(relative_point, point)) for point in points
		if distance(relative_point, point) < THRESHOLD]

	# This is a mapreduce operation mapping each of the above (point, distance) tuples into
	#... a weight, and then reducing that list of weights by simple summation. It would be
	#... a bit simpler to do the mapping step in the above list comprehension, but then you
	#... lose the ability to do more clever things with the point data if you want to later
	cumulative_sum = reduce((lambda a, b: a + b),
		map((lambda (point, dist): weight(point.val, dist)), in_range))

	return cumulative_sum / len(in_range)


def deinterpolate(points, upper_left, lower_right):
	result = {
		"upper_left":	Point(x = upper_left.x, y = upper_left.y),
		"upper_right":	Point(x = lower_right.x, y = upper_left.y),
		"lower_left":	Point(x = upper_left.x, y = lower_right.y),
		"lower_right":	Point(x = lower_right.x, y = lower_right.y),
		"center":		Point(x = (upper_left.x + lower_right.x) / 2.0,
			y = (upper_left.y + lower_right.y) / 2.0)
	}

	for key in result:
		result[key].val = calc_point(result[key], points)

	return result
