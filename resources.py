
from flask_restful import Resource
import Pyro4
from ast import literal_eval

from business import Game

games = {}

@Pyro4.expose
class GameRemoteObject(object):
    def create(self, name):
        #return 'alane' #foquinha...
        games[name] = Game(name)
        return {'success': True, 'name': name}

    def join(self, name):
        if name in games:
            return games[name].new_player()
        else:
            return {'success': False, 'message': 'No game found for name ' + name}

    def game_status(self, name):
        if name in games:
            return games[name].get_status()
        else:
            return {'success': False, 'message': 'No game found for name ' + name}

    def pass_turn(self, name):
        if name in games:
            return games[name].pass_turn()
        else:
            return {'success': False, 'message': 'No game found for name ' + name}

    def make_a_move(self, name, _id, from_point, to_point):
        if name in games:
            return games[name].make_a_move(int(_id), literal_eval(from_point), literal_eval(to_point))
        else:
            return {'success': False, 'message': 'No game found for name ' + name}

    def possible_moves(self, name, _id, current_point):
        if name in games:
            return games[name].possible_moves(int(_id), literal_eval(current_point))
        else:
            return {'success': False, 'message': 'No game found for name ' + name}

    def giveup(self, name, _id):
        if name in games:
            return games[name].giveup(int(_id))
        else:
            return {'success': False, 'message': 'No game found for name ' + name}

# class InitGame(Resource):
#     #Create a new game
#     def get(self, name):
#         if name in games: 
#             return {"message": "Name already registered: " + name}, 409
#         else:
#             games[name] = {
#                 'status': 'initiating',
#                 'turn': 1,
#                 1: {
#                     'tiles': [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)],
#                     'victory': [(17, 1), (16, 1), (16, 2), (15, 1), (15, 2), (15, 3), (14, 1), (14, 2), (14, 3), (14, 4)]
#                 }
#             }
#             return {"id": 1, "name": name}, 201
    
#     #Join an existing game
#     def link(self, name):
#         if name in games:
#             if games[name]['status'] == 'initiating':
#                 games[name][2] = {
#                     'tiles': [(17, 1), (16, 1), (16, 2), (15, 1), (15, 2), (15, 3), (14, 1), (14, 2), (14, 3), (14, 4)],
#                     'victory': [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
#                 }
#             else:
#                 return {"message": "Cannot join. Game already started."}
#         else:
#             return {"id": 2}, 200


# class PlayGame(Resource):
#     #Query the game status
#     def get(self, name):
#         if name in games:
#             game = games[name]
#             return {"status": game['status'], "turn": game['turn']}, 200
#         else:
#             return {"message": "No game with name " + name}, 404

#     #Give up the game
#     def unlink(self, name, _id):
#         if name in games:
#             game = games[name]

#             if _id in games[name]:
#                 return {"status": game['status'], "turn": game['turn']}, 200
#             else:
#                 return {"message": "No player with id " + _id}, 404
#         else:
#             return {"message": "No game with name " + name}, 404

#     #Execute a move on the game, if valid
#     def patch(self, name, _id, from_p, to_p):
#         try:
#             iid = int(_id, 10)
#             from_tuple = (int(from_p.slice(1, 2), 10), int(from_p.slice(3, 4), 10))
#             to_tuple = (int(to_p.slice(1, 2), 10), int(to_p.slice(3, 4), 10))
            
#             if name not in games:
#                 return {"message": "No game with name " + name}, 404

#             game = games[name]

#             if game['status'] == 'over':
#                 return {"message": "Game is over"}, 400

#             if iid not in game:
#                 return {"message": "No player with id " + _id}, 404
            
#             if iid != game['turn']:
#                 return {"message": "Not player's turn"}, 400

#             player = game[iid]
            
#             if not tile_exists(to_tuple) or not has_tile(player, from_tuple):
#                 return {"message": "Invalid tiles"}, 400
            
#             if not is_move_valid(to_tuple, from_tuple):
#                 return {"message": "Bad move"}, 400

#             player['tiles'].remove(from_tuple)
#             player['tiles'].append(to_tuple)

#             if game['status'] == 'initiating':
#                 game['status'] = 'ongoing'

#             if all(elem in player['tiles'] for elem in player['victory']):
#                 game['status'] = 'over'
#             elif (iid + 1) in game[name]:
#                 game['turn'] = iid + 1
#             else:
#                 game['turn'] = 1

#             return {'status': game['status']}, 200
#         except:
#             return 400
