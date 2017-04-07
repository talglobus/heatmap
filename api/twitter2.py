from twython import Twython, TwythonStreamer

APP_KEY = "1GMEj6PR6SVWyHmSbjhhHfcaO"
APP_SECRET = "fVc3ywjjkGHKwulOQGDdE5FoPHPkuKYrc4jeN5Rhda3iPztwJ7"

twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens() # This might need a callback url

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

print auth['auth_url']

oauth_verifier = input("What is the oauth user verification code?	")
print(oauth_verifier)

final_auth = twitter.get_authentication_tokens(int(oauth_verifier))

new_token = final_auth['oauth_token']
new_secret = final_auth['oauth_token_secret']

class Streamer(TwythonStreamer):
	def on_success(self, data):
		print data.keys()
		if 'text' in data:
			print data['text'].encode('utf-8')

	def on_error(self, status_code, data):
		print "Error: " + str(status_code) + data
		self.disconnect()

stream = Streamer(APP_KEY, APP_SECRET, new_token, new_secret)

stream.statuses.filter(track="twitter")