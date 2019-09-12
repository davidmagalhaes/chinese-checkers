from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

# from resources import InitGame
# from resources import PlayGame
from resources import GameRemoteObject

import Pyro4

# python -m Pyro4.naming

def start_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(GameRemoteObject)
    ns.register('checkers', str(uri))
    print(f'Ready to listen')
    daemon.requestLoop()

if __name__ == '__main__':
    try:
        pass
        # app = Flask(__name__)
        # api = Api(app)

        # api.add_resource(InitGame, '/game/init/<string:name>')
        # api.add_resource(PlayGame, '/game/play/<string:name>/<string:_id>/<string:from_p>/<string:to_p>')

        #start_server()
        # app.run(port=5002, debug=True)
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! (:')








