import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from time import time

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
stop = False
count = 0
loss = 0

class StdOutListener(StreamListener):

	def on_data(self, datum):
		global count, stop, loss

		count += 1
		datum = json.loads(datum)
		if ('geo' in datum and datum['geo'] <> None):
			data.append(datum)
		if ('limit' in datum):
			loss = datum['limit']['track']
		if count % 200 == 1 && DEBUGGING:
			print "Total tweets stored: " + str(len(data)) + ". Due to rate limiting, you've missed " + str(loss) + " tweets. Recent: " + str(len(recent_tweets()))
		return (not stop)

	def on_error(self, status):
		if DEBUGGING:
			print "Error: " + str(status)

l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream = Stream(auth, l)

def go():
	stream.filter(locations=[-180, -90, 180, 90], async=False)

def stop():
	global stop
	stop = True

def recent_tweets():
	now = time() * 1000

	# List comprehension to produce simplified tweet representation with three necessary values,
	#... tweet text, coordinates and millisecond timestamp, for all tweets that fall in the
	#... `ROLLING_INTERVAL`. TODO: Older tweets should really be removed
	recents = [{'text': datum['text'], 'coordinates': datum['geo']['coordinates'], 'time': datum['timestamp_ms']} for datum in data
		if now - int(datum['timestamp_ms']) < ROLLING_INTERVAL * 1000]

	return recents

def show(datum):
	print (datum['text'] + ": " + datum['geo']['coordinates'] + " at " + type(datum['timestamp_ms']))