up um servidor de nome
    python -m Pyro4.naming

cadastrar um instancia no servidor de nomes

´´´
    def start_server():
        daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()
        uri = daemon.register(GameRemoteObject) ****
        ns.register('checkers', str(uri))
        print(f'Ready to listen')
        daemon.requestLoop()

´´´

startar o servidor 
´´´
    if __name__ == '__main__':
        try:
            app = Flask(__name__)
            api = Api(app)

            api.add_resource(InitGame, '/game/init/<string:name>')
            api.add_resource(PlayGame, '/game/play/<string:name>/<string:_id>/<string:from_p>/<string:to_p>')

            start_server()
            app.run(port=5002, debug=True)
        except (KeyboardInterrupt, EOFError):
            print('Goodbye! (:')
´´´

python -m Pyro4.utils.httpgateway -e 'checkers'

just call seu client js