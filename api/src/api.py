from flask import Flask
from flask_restful import Resource, Api, reqparse
from watson import empathize
from twitter import get_tweets
from position import Point, distance
from deinterpolate_text import deinterpolate
# from partialInput.py import PartialInput


def main():
	print("working")
	print("yupples")
	p = Point(x = 5, y = 6, val = 2)
	print(p)

# app = Flask(__name__)
# api = Api(app)
#
# app.config['ERROR_404_HELP'] = False
#
# parser = reqparse.RequestParser()
# parser.add_argument('upLat', type=float, help='Latitude coordinate of top of requested search area')
# parser.add_argument('downLat', type=float, help='Latitude coordinate of bottom of requested search area')
# parser.add_argument('leftLong', type=float, help='Longitude coordinate of left of requested search area')
# parser.add_argument('rightLong', type=float, help='Longitude coordinate of right of requested search area')
#
# class Full(Resource):
# 	def get(self):
# 		return {"send": "this"}
#
# class Partial(Resource):
# 	def get(self):
# 		args = parser.parse_args(strict=True)
#
#
#
#
# api.add_resource(Full, '/Full')
# api.add_resource(Partal, '/Partial')
#
# if __name__ == "__main__":
# 	app.run(debug=True)

if __name__ == "__main__":
	main()