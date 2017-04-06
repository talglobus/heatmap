from flask import Flask
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
# from partialInput.py import PartialInput

app = Flask(__name__)
api = Api(app)

app.config['ERROR_404_HELP'] = False

partialArgs = {
	'upLat': fields.Float(required=True)
	'downLat': fields.Float(required=True)
	'leftLong': fields.Float(required=True)
	'rightLong': fields.Float(required=True)
}

parser = reqparse.RequestParser()
parser.add_argument('upLat', type=int, help='Latitude coordinate of top of requested search area')
parser.add_argument('downLat', type=int, help='Latitude coordinate of bottom of requested search area')
parser.add_argument('leftLong', type=int, help='Longitude coordinate of left of requested search area') 
parser.add_argument('rightLong', type=int, help='Longitude coordinate of right of requested search area')
args = parser.parse_args(strict=True)

class Full(Resource):
	def get(self):
		return {"send": "this"}

class Partial(Resource):
	def get(self, upLat, downLat, leftLong, rightLong):
		#

api.add_resource(Full, '/Full')
api.add_resource(Partal, '/Partial')

if __name__ == "__main__":
	app.run(debug=True)