import resources
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

api.add_resource(resources.InitGame, '/game/init/<string:name>')
api.add_resource(resources.PlayGame, '/game/play/<string:name>/<string:_id>/<string:from_p>/<string:to_p>')

app.run(port=5002, debug=True)
