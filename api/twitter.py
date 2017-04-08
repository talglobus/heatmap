import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from time import time
from position import Point, calc_needed, in_box

# Twitter API Credentials
ACCESS_TOKEN = "845835746254598144-OrWne9CKWvFJwPMKCLkFdBdJROoUFW2"
ACCESS_TOKEN_SECRET = "2L6bP22O249kVfx2Vtk1PokHfwXatbDkBv83uTuTyxgjf"
CONSUMER_KEY = "1GMEj6PR6SVWyHmSbjhhHfcaO"
CONSUMER_SECRET = "fVc3ywjjkGHKwulOQGDdE5FoPHPkuKYrc4jeN5Rhda3iPztwJ7"

# Interval of last x seconds to be used for real-time evaluation
ROLLING_INTERVAL = 600

# Prints updates in the following form to stdout roughly every 5 seconds:
# Total tweets stored: 35472. Due to rate limiting, you've missed 15514 tweets. Recent: 3547
DEBUGGING = True

# A listing of the most common words in English for filtering
COMMON = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not',
	'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
	'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
	'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make',
	'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
	'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only',
	'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work',
	'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day',
	'most', 'us']

data = []
going = True
count = 0
loss = 0


class StdOutListener(StreamListener):

	def on_data(self, datum):
		global count, going, loss

		count += 1
		datum = json.loads(datum)
		if 'geo' in datum and datum['geo'] is not None:
			data.append(datum)
		if 'limit' in datum:
			loss = datum['limit']['track']
		if count % 200 == 1 and DEBUGGING:
			print(f"Total tweets stored: {len(data)}. Due to rate limiting, you've missed {loss}"
				f"tweets. Recent: {len(recent_tweets())}")
		return going

	def on_error(self, status):
		if DEBUGGING:
			print(f"Error: {status}")

l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream = Stream(auth, l)


def go():
	stream.filter(locations=[-180, -90, 180, 90], async=False)


def stop():
	global going
	going = False


def recent_tweets():
	now = time() * 1000

	# List comprehension to produce simplified tweet representation with three necessary values,
	# tweet text, coordinates and millisecond timestamp, for all tweets that fall in the
	# `ROLLING_INTERVAL`. TODO: Older tweets should really be removed
	recents = [{'text': datum['text'], 'coordinates': datum['geo']['coordinates'],
				'time': datum['timestamp_ms']} for datum in data
		if now - int(datum['timestamp_ms']) < ROLLING_INTERVAL * 1000]

	return recents


def show(datum):
	print(f"{datum['text']}: {datum['geo']['coordinates']} at {type(datum['timestamp_ms'])}")


# This is the primary function used from this module. Plug in `upper_left` and `lower_right`
# corners for the viewport, and the minimum number of tweets needed for data deinterpolation,
# and it returns a list of all necessary and relevant tweets, each a condensed dictionary of
# only necessary information.
#
# Note that the approach here for `min_points` could be far more clever. The function accepts
# the desired number of tweets for data deinterpolation as `min_points`, and from all the tweets
# in the rectangle defined by `upper_left`, `lower_right`, and the threshold around those corners
# widening the rectangle, takes the `min_points` most recent tweets, going back as far in time
# is necessary to exactly meet `min_points` tweets worth of data. The actual number of tweets
# used here really shouldn't be set exactly to min_points, rather it should go up and down as
# best suits the data, but then you're getting into a complex model just to figure out how many
# data points to use in any particular case. TODO: Figure out if that's a good idea for later
#
# Note also that not all of these points will actually be included in the final calculation,
# because the rectangle used to limit the tweets considered, defined by corners
# `needed['threshold_upper_left']` and `needed['threshold_lower_right']` as calculated by
# adding a `threshold`-wide buffer around the rectangle defined by `upper_left` and `lower_right`
# actually includes areas beyond the thresholds of the result points deinterpolated from these
# input points. Thus `min_points` needs to be at least as large, and ideally safely larger than
# the actual minimum number of tweets needed for a good deinterpolation
def get_tweets(upper_left, lower_right, min_points):
	now = time() * 1000

	needed = calc_needed(upper_left = upper_left, lower_right = lower_right)

	# List comprehension in a function in a built-in slice. First, the list comprehension
	# converts the complex dictionary input into a smaller dictionary with the only three
	# needed values: tweet text, coordinates, and timestamp (in milliseconds), and filters by
	# items corresponding to points that fall within the needed rectangle. Thus at this stage,
	# any points completely out of the viewport and threshold area around it are eliminated
	# from consideration, limiting the returned tweets to only those that are geographically
	# relevant.
	#
	# Then, the built-in `sorted()` function sorts the list by decreasing timestamp,
	# so that the first elements in the list will be the most recent tweets.
	#
	# Finally, the `[:min_points]` at the end takes the first `min_points` elements of the list,
	# as the `min_points` most recent tweets.
	tweets = sorted([{'text': datum['text'], 'coordinates': datum['geo']['coordinates'],
			   'time': datum['timestamp_ms']} for datum in data if in_box(
				Point(x = datum['coordinates'][1], y = datum['coordinates'][0]),
				upper_left = needed['threshold_upper_left'],
				lower_right = needed['threshold_lower_right'])], key=lambda item: item['time'],
					reverse=True)[:min_points]

	# Calculate the time interval used in this case. This is the range of time in which all
	# tweets appear. A smaller number therefore means more recent tweets, and will tend to
	# correspond to larger viewport areas, and as a user zooms in, the tweets by necessity
	# are no longer able to be as fresh and still maintain enough tweets for data deinterpolation
	interval = now - tweets[-1]['time']

	return {'tweets': tweets, 'interval': interval}
