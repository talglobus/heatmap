from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Test(Resource):
	def get(self):
		return {"send": "this"}

api.add_resource(Test, '/')

if __name__ == "__main__":
	app.run(debug=True)