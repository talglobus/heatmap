CONSUMER_KEY = "1GMEj6PR6SVWyHmSbjhhHfcaO"
CONSUMER_SECRET = "fVc3ywjjkGHKwulOQGDdE5FoPHPkuKYrc4jeN5Rhda3iPztwJ7"

def oauth_req(url, key, secret, http_method="GET", post_body=””, http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

home_timeline = oauth_req('https://stream.twitter.com/1.1/statuses/sample.json', 'abcdefg', 'hijklmnop' )