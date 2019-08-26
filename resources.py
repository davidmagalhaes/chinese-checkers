
from flask_restful import Resource

board_sizes = [
    1,
    2,
    3,
    4,
    13,
    12,
    11,
    10,
    9,
    10,
    11,
    12,
    13,
    4,
    3,
    2,
    1 
]

games = {}

def tile_exists(tuple):
    if len(board_sizes) >= tuple[0]:
        if len(board_sizes[tuple[0]]) >= tuple[1]:
            return True
    return False

def has_tile(player, tile):
    return player.tiles.count(tile)

def is_move_valid(from_tile, to_tile):
    return abs(from_tile[0] - to_tile[0]) <= 1 and abs(from_tile[1] - to_tile[1]) <= 1

class InitGame(Resource):
    #Create a new game
    def get(self, name):
        if name in games: 
            return {"message": "Name already registered: " + name}, 409
        else:
            games[name] = {
                'status': 'initiating',
                'turn': 1,
                1: {
                    'tiles': [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)],
                    'victory': [(17, 1), (16, 1), (16, 2), (15, 1), (15, 2), (15, 3), (14, 1), (14, 2), (14, 3), (14, 4)]
                }
            }
            return {"id": 1, "name": name}, 201
    
    #Join an existing game
    def link(self, name):
        if name in games:
            if games[name]['status'] == 'initiating':
                games[name][2] = {
                    'tiles': [(17, 1), (16, 1), (16, 2), (15, 1), (15, 2), (15, 3), (14, 1), (14, 2), (14, 3), (14, 4)],
                    'victory': [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
                }
            else:
                return {"message": "Cannot join. Game already started."}
        else:
            return {"id": 2}, 200


class PlayGame(Resource):
    #Query the game status
    def get(self, name):
        if name in games:
            game = games[name]
            return {"status": game['status'], "turn": game['turn']}, 200
        else:
            return {"message": "No game with name " + name}, 404

    #Execute a move on the game, if valid
    def patch(self, _id, name, from_p, to_p):
        try:
            iid = int(_id, 10)
            from_tuple = (int(from_p.slice(1, 2), 10), int(from_p.slice(3, 4), 10))
            to_tuple = (int(to_p.slice(1, 2), 10), int(to_p.slice(3, 4), 10))
            
            if name not in games:
                return {"message": "No game with name " + name}, 404

            game = games[name]

            if game['status'] == 'over':
                return {"message": "Game is over"}, 400

            if iid not in game:
                return {"message": "No player with id " + _id}, 404
            
            if iid != game['turn']:
                return {"message": "Not player's turn"}, 400

            player = game[iid]
            
            if not tile_exists(to_tuple) or not has_tile(player, from_tuple):
                return {"message": "Invalid tiles"}, 400
            
            if not is_move_valid(to_tuple, from_tuple):
                return {"message": "Bad move"}, 400

            player['tiles'].remove(from_tuple)
            player['tiles'].append(to_tuple)

            if game['status'] == 'initiating':
                game['status'] = 'ongoing'

            if all(elem in player['tiles'] for elem in player['victory']):
                game['status'] = 'over'
            elif (iid + 1) in game[name]:
                game['turn'] = iid + 1
            else:
                game['turn'] = 1

            return {'status': game['status']}, 200
        except:
            return 400