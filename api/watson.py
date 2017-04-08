import json
from watson_developer_cloud import ToneAnalyzerV3
import hashlib

tone_analyzer = ToneAnalyzerV3(
   username='41cc5265-41f0-4383-95f1-3faae972d1c0',
   password='WjBkBwRyMZJD',
   version='2016-05-19')


class Sample(object):

	def __init__(self, text, result=None):
		self.text = text
		self.hash = self._hash(text)
		self.result = result

	def _hash(self, text):
		return hashlib.sha1(text.encode()).hexdigest()

data = {}

def analyze(text):
	sample = Sample(text)
	out = tone_analyzer.tone(text=text)
	sample.result = out
	data[sample.hash] = sample
	
	return out


def empathize(text):
	analysis = analyze(text)
	result = {}

	for emotion in analysis:
		result[emotion["tone_id"]] = emotion["score"]

	return result
	


