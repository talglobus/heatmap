# This provides a function, `deinterpolate()`, which takes coordinates for upper left hand and
# bottom right hand corners, along with a series of points (x, y, value), and finds five
# point values, namely the upper left, upper right, lower left, lower right and middle point

import math
from position import Point, distance, calc_needed


# Because weighting works by repeating text, and repetition must be an integer number of times,
# weights are scaled by this value, so text will appear between 0 and 20 times
MAX_REPEAT = 20


# This function is the bread and butter of this module, determining how, given a point's value
# and the distance from it to the result point, it is weighted into the value assigned to the
# result. Note that the values being weighted are text, and so all weighting takes the form
# of text repeated by a multiplier determined by the weight.
#
# There are a few rules that need to be followed for this to be a good weighting:
#
# 1) If all input values are the same, all result values anywhere in the range should match
#	 - This means that if the input points are all the same text, all result points should be the
#		same text, in this case repeated MAX_REPEAT times, regardless of where they are in
#		relation to the input points
# 2) Result values shouldn't be biased up or down because they happen to not be near input points
#	 - This means that overall weighting should average to some constant at all points, like
#		how at any point in the unit circle, sin^2(theta) + cos^2(theta) is ALWAYS 1
# 3) The closer a result point to an input point, the greater weight the input point should have
#	on the result point. This just means that closer points are weighted above farther points
def weight(val, dist, threshold):
	return val * int(round((threshold - dist) / threshold * MAX_REPEAT))


def calc_point(result_point, points, threshold):
	# This list comprehension constructs a string that contains the concatenated text from all
	# input points within range `THRESHOLD`, repeated for weighting up to `MAX_REPEAT` times
	# depending on distance between the `result_point` and the input `point` as described above
	# @see weight
	cumulative_text = sum([weight(point.val, distance(result_point, point), threshold)
						   for point in points if distance(result_point, point) < threshold])

	return cumulative_text.strip()	# Remove trailing space left from spaces appended earlier


def append_spaces(points):
	return map((lambda point: Point(x = point.x, y = point.y, val = point.val + " ")), points)


def deinterpolate(points, upper_left, lower_right):
	threshold = calc_needed(upper_left = upper_left, lower_right = lower_right)["threshold"]

	points = append_spaces(points)

	result = {
		"upper_left":	Point(x = upper_left.x, y = upper_left.y),
		"upper_right":	Point(x = lower_right.x, y = upper_left.y),
		"lower_left":	Point(x = upper_left.x, y = lower_right.y),
		"lower_right":	Point(x = lower_right.x, y = lower_right.y),
		"center":		Point(x = (upper_left.x + lower_right.x) / 2.0,
			y = (upper_left.y + lower_right.y) / 2.0)
	}

	for key in result:
		result[key].val = calc_point(result[key], points, threshold)

	return result
