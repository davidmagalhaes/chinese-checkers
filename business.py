class Game(object):

    start_positions = {
        1 : [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)],
        2 : [(17, 1), (16, 1), (16, 2), (15, 1), (15, 2), (15, 3), (14, 1), (14, 2), (14, 3), (14, 4)]
    }

    victory_conditions = {
        1 : [(17, 1), (16, 1), (16, 2), (15, 1), (15, 2), (15, 3), (14, 1), (14, 2), (14, 3), (14, 4)],
        2 : [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
    }

    def __init__(self, name):
        self.name = name
        self.turn = 1
        self.status = 'initiating'
        self.players_count = 0
        self.players = []
        self.board = [
                           [0],
                          [0, 0],
                         [0, 0, 0],
                        [0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0],
                         [0, 0, 0],
                          [0, 0],
                            [0]
        ]
    
    def new_player(self):
        if self.status == 'initiating':
            new_player = {
                'status': 'playing',
                'jumping': False,
                'id': self.players_count+1
            }

            self.players.append(new_player)
            self.players_count += 1

            for tupl in Game.start_positions[new_player['id']]:
                put_on_board(self, tupl, new_player['id'])

            return {'success': True, 'id': new_player['id']}
        elif self.status == 'over':
            return {'success': False, 'message': "Game is over"}
        else:
            return {'success': False, 'message': "Game already started"}

    def pass_turn(self, _id):
        if self.status == 'over':
            return {'success': False, 'message': "Game is over"}
        if self.turn != _id:
            return {'success': False, 'message': "Not the player's turn"}

        winner = [player for player in self.players if player['status'] == 'victorious']

        if len(winner) == 1:
            self.status = 'over'
            for defeated_player in [player for player in self.players if player['status'] != 'victorious']:
                defeated_player['status'] = 'defeated'

            return {'success': True, 'winner': winner[0]['id']}
        else:
            next_id = ((_id - 1) % len(self.players)) + 2

            while(get_player(self, next_id)['status'] == 'defeated'):
                next_id = ((next_id - 1) % len(self.players)) + 2

            self.turn = next_id

            if self.status == 'initiating':
                self.status = 'ongoing'
            
            player = get_player(self, _id)
            player['jumping'] = False

        return {'success': True, 'turn': next_id}

    def make_a_move(self, _id, from_point, to_point):
        if self.status == 'over':
            return {'success': False, 'message': "Game is over"}
        if self.turn != _id:
            return {'success': False, 'message': "Not the player's turn"}

        player = get_player(self, _id)

        if has_tile(self, _id, from_point) and self.possible_moves(_id, from_point)['moves'].count(to_point) > 0:
            move_is_a_jump = is_a_jump(from_point, to_point)

            if player['jumping'] and not move_is_a_jump:
                return {'success': False, 'message': "Bad Move"}
            elif move_is_a_jump:
                player['jumping'] = True
            
            put_on_board(self, from_point, 0)
            put_on_board(self, to_point, _id)

            if all(has_tile(self, _id, tile) for tile in Game.victory_conditions[_id]):
                player['status'] = 'victorious'
                return self.pass_turn(_id)
            elif not player['jumping']:
                return self.pass_turn(_id)
            elif player['jumping'] and len(self.possible_moves(_id, to_point)['moves']) == 0:
                return self.pass_turn(_id)

            return {'success': True, 'turn': _id}
        else:
            return {'success': False, 'message': "Bad Move"}

    def possible_moves(self, _id, current_point):
        if self.status == 'over':
            return {'success': False, 'message': "Game is over"}

        player = get_player(self, _id)
        move_list = []
        all_simple_moves = [
            (current_point[0], current_point[1]-1), 
            (current_point[0], current_point[1]+1), 
            (current_point[0]+1, current_point[1]), 
            (current_point[0]+1, current_point[1]+1), 
            (current_point[0]-1, current_point[1]), 
            (current_point[0]-1, current_point[1]+1)
        ]
        all_jump_moves = [
            (current_point[0], current_point[1]-2), 
            (current_point[0], current_point[1]+2), 
            (current_point[0]+2, current_point[1]-1), 
            (current_point[0]+2, current_point[1]+1), 
            (current_point[0]-2, current_point[1]-1), 
            (current_point[0]-2, current_point[1]+1)
        ]

        if not player['jumping']:
            move_list.extend([item for item in all_simple_moves if tile_exists(self, item) and tile_is_available(self, item)])

        #A jump move needs the intermediate tile to be occupied. To make things simple, 
        #the intermediate of a jump move in the list 'all_jump_moves' is the element of 'all_simple_moves' of same index.
        for i, item in enumerate(all_jump_moves):
            if tile_exists(self, item) and tile_is_available(self, item) and not tile_is_available(self, all_simple_moves[i]):
                move_list.append(item)
        
        return {'success': True, 'moves': move_list}

    def giveup(self, _id):
        if self.turn != _id:
            return {'success': False, 'message': "Not the player's turn"}

        if self.status == 'initiating':
            del self.players[_id - 1]
            return {'success': True}
        elif self.status == 'ongoing':
            player = get_player(self, _id)
            player['status'] = 'defeated'

            active_players = [player for player in self.players if player['status'] == 'playing']

            if len(active_players) == 1:
                active_players[0]['status'] = 'victorious'

            return self.pass_turn(_id)
        elif self.status == 'over':
            return {'success': False, 'message': "Game is over"}

    def get_status(self):
        game_status = {
            'status': self.status, 
            'turn': self.turn, 
            'player_count': self.players_count, 
            'defeated_players': [player['id'] for player in self.players if player['status'] == 'defeated']
        }

        if self.status == 'over':
            winner = [player for player in self.players if player['status'] == 'victorious']
            game_status['winner'] = winner[0]['id']
        
        return game_status

def tile_is_available(game: Game, tupl):
    return game.board[tupl[0]-1][tupl[1]-1] == 0

def tile_exists(game : Game, tupl):
    if tupl[0] > 0 and len(game.board) >= tupl[0]:
        if tupl[1] > 0 and len(game.board[tupl[0]-1]) >= tupl[1]:
            return True
    return False

def has_tile(game : Game, player_id, tile):
    return game.board[tile[0]-1][tile[1]-1] == player_id

def is_a_jump(from_point, to_point):
    return (from_point[0] == (to_point[0] - 2) or from_point[0] == (to_point[0] + 2) or 
        (from_point[1] == to_point[1] - 2) or (from_point[1] == to_point[1] + 2))

def put_on_board(game, tupl, val):
    game.board[tupl[0]-1][tupl[1]-1] = val

def get_player(game, _id):
    return game.players[_id - 1]