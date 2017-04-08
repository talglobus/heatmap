import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

ACCESS_TOKEN = "845835746254598144-OrWne9CKWvFJwPMKCLkFdBdJROoUFW2"
ACCESS_TOKEN_SECRET = "2L6bP22O249kVfx2Vtk1PokHfwXatbDkBv83uTuTyxgjf"
CONSUMER_KEY = "1GMEj6PR6SVWyHmSbjhhHfcaO"
CONSUMER_SECRET = "fVc3ywjjkGHKwulOQGDdE5FoPHPkuKYrc4jeN5Rhda3iPztwJ7"

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

class StdOutListener(StreamListener):

	def on_data(self, datum):
		global count
		global stop
		count += 1
		datum = json.loads(datum)
		if ('geo' in datum and datum['geo'] <> None):
			data.append(datum)
			# print (datum['text'] + ": " + datum['geo']['coordinates'] + " at " + type(datum['timestamp_ms']))
		if ('limit' in datum):
			print "You are being rate limited. You've missed " + str(datum['limit']['track']) + " tweets"
		if count % 100 == 1:
			print "Total tweets stored: " + str(len(data))
		return (not stop)

	def on_error(self, status):
		print "Error: " + str(status)

l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream = Stream(auth, l)

def go():
	stream.filter(locations=[-180, -90, 180, 90], async=False)

def s():
	stop = True