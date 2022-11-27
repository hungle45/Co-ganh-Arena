from collections import defaultdict
import copy

import numpy as np

class State:
    def __init__(self, board: list, player: int):
        self.player = player
        self.board = np.array(board)
        self.height = self.board.shape[0]
        self.width = self.board.shape[1]

    def __eq__(self, other):
        return np.array_equal(self.board,other.board) \
            and self.player == other.player

    def check_winning_state(self):
        # return: one of below:
        #           (1)  1: player 1 win
        #           (2) -1: player 2 win
        #           (3)  0: continue
        result = 0
        if np.all(self.board < 1):
            result = -1
        elif np.all(self.board > -1):
            result = 1
        return result

class Problem:
    def __init__(self):
        self.init_state = State(
            board=[[ 1,  1,  1,  1,  1],
                   [ 1,  0,  0,  0,  1],
                   [ 1,  0,  0,  0, -1],
                   [-1,  0,  0,  0, -1],
                   [-1, -1, -1, -1, -1]],
            player = 1
        )

    def get_possible_moves(self, state:State):
        '''
        Get all possible moves for given state.

        Input
        ----------
            state: input State.
            
        Output
        ----------
            possible_move: output dict of possible move with key is the starting 
                           position, value is a list of the destination position.
                           eg. {
                            (1,2): [(2,2),(1,1),...]
                            ...
                           }
            
        '''
        def compare_pos(pos: tuple):
            return pos[0] + pos[1] * 1000

        dictionary = dict({})
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                position = []
                if(state.board[coor_y, coor_x] == state.player):

                    left = bool(state.board[coor_y, max(0, coor_x - 1)])
                    right = bool(state.board[coor_y, min(coor_x + 1, state.width - 1)])
                    up = bool(state.board[max(0, coor_y - 1), coor_x])
                    down = bool(state.board[min(coor_y + 1, state.height - 1), coor_x])
                    if not left:
                        position.append((coor_y, coor_x - 1))
                    if not right:
                        position.append((coor_y, coor_x + 1))
                    if not up:
                        position.append((coor_y - 1, coor_x))
                    if not down:
                        position.append((coor_y + 1, coor_x))
                    if ((coor_x + coor_y) % 2 == 0):
                        top_left = bool(state.board[max(0, coor_y - 1), max(0, coor_x - 1)])
                        top_right = bool(state.board[max(0, coor_y - 1), min(coor_x + 1, state.width - 1)])
                        bottom_left = bool(state.board[min(coor_y + 1, state.height - 1), max(0, coor_x - 1)])
                        bottom_right = bool(state.board[min(coor_y + 1, state.height - 1), min(coor_x + 1, state.width - 1)])
                        if not top_left:
                            position.append((coor_y - 1, coor_x - 1))
                        if not top_right:
                            position.append((coor_y - 1, coor_x + 1))
                        if not bottom_left:
                            position.append((coor_y + 1, coor_x - 1))
                        if not bottom_right:
                            position.append((coor_y + 1, coor_x + 1))

                if (position):
                    dictionary[(coor_y, coor_x)] = sorted(position, key= compare_pos)
        return dictionary

    def capture(self, state: State, pos: tuple):
        player = state.board[pos]
        coor_y = pos[0]
        coor_x = pos[1]
        left = state.board[coor_y, max(0, coor_x - 1)]
        right = state.board[coor_y, min(coor_x + 1, state.width - 1)]
        up = state.board[max(0, coor_y - 1), coor_x]
        down = state.board[min(coor_y + 1, state.height - 1), coor_x]
        remove = []
        is_left, is_right, is_up, is_down = False, False, False, False

        if (left == -player):
            if state.board[coor_y, max(0, coor_x - 2)] == player:
                remove.append((coor_y, coor_x - 1)) #Remove left opponent
                is_left = True
        if (right == -player):
            if state.board[coor_y, min(coor_x + 2, state.width - 1)] == player:
                remove.append((coor_y, coor_x + 1)) #Remove right opponent 
                is_right = True
        if ((left == right) & (left == -player)):
            if not is_left:
                remove.append((coor_y, coor_x - 1))
            if not is_right:
                remove.append((coor_y, coor_x + 1))
        
        if (up == -player):
            if state.board[max(0, coor_y - 2), coor_x] == player:
                remove.append((coor_y - 1, coor_x)) #Remove up opponent
                is_up = True
        if (down == -player):
            if state.board[min(coor_y + 2, state.height - 1), coor_x] == player:
                remove.append((coor_y + 1, coor_x)) #Remove down opponent 
                is_down = True
        if ((up == down) & (up == -player)):
            if not is_up:
                remove.append((coor_y - 1, coor_x))
            if not is_down:
                remove.append((coor_y + 1, coor_x))

        if ((coor_x + coor_y) % 2 == 0):
            top_left = state.board[max(0, coor_y - 1), max(0, coor_x - 1)]
            top_right = state.board[max(0, coor_y - 1), min(coor_x + 1, state.width - 1)]
            bottom_left = state.board[min(coor_y + 1, state.height - 1), max(0, coor_x - 1)]
            bottom_right = state.board[min(coor_y + 1, state.height - 1), min(coor_x + 1, state.width - 1)]
            is_top_left, is_top_right, is_bottom_left, is_bottom_right = False, False, False, False
            
            if (top_left == -player):
                if state.board[max(0, coor_y - 2), max(0, coor_x - 2)] == player:
                    remove.append((coor_y - 1, coor_x - 1)) #Remove top left opponent
                    is_top_left = True
            if (bottom_right == -player):
                if state.board[min(coor_y + 1, state.height - 1), min(coor_x + 1, state.width - 1)] == player:
                    remove.append((coor_y, coor_x + 1)) #Remove bottom right opponent 
                    is_bottom_right = True
            if ((top_left == bottom_right) & (top_left == -player)):
                if not is_top_left:
                    remove.append((coor_y - 1, coor_x - 1))
                if not is_bottom_right:
                    remove.append((coor_y + 1, coor_x + 1))
            
            if (top_right == -player):
                if state.board[max(0, coor_y - 1), min(coor_x + 1, state.width - 1)] == player:
                    remove.append((coor_y - 1, coor_x + 1)) #Remove top right opponent
                    is_top_right = True
            if (bottom_left == -player):
                if state.board[min(coor_y + 1, state.height - 1), max(0, coor_x - 1)] == player:
                    remove.append((coor_y + 1, coor_x - 1)) #Remove bottom left opponent 
                    is_bottom_left = True
            if ((top_right == bottom_left) & (top_right == -player)):
                if not is_top_right:
                    remove.append((coor_y - 1, coor_x + 1))
                if not is_bottom_left:
                    remove.append((coor_y + 1, coor_x - 1))            
        return remove

    def move(self, state: State, action, inplace=False):
        '''
        Do action.

        Input
        ----------
            state: input State.
            action: eg. ((1,1),(1,2)).
            inplace: False if return copy of state and otherwise.
            
        Output
        ----------
            state: state after do action.
                   None if inplace is True.
            
        '''
        if not inplace:
            state = copy.deepcopy(state)
        state.board[action[1]] = state.board[action[0]]
        state.board[action[0]] = 0
        remove_list = self.capture(state, action[1])
        for pos in remove_list:
            state.board[pos] = 0
        state.player *= -1

        if not inplace:
            return state

    def move_if_possible(self, state:State, action, inplace=False):
        '''
        Do action if possible.

        Input
        ----------
            state: input State.
            action: eg. ((1,1),(1,2)).
            inplace: False if return copy of state and otherwise.
            
        Output
        ----------
            can_do: true if can do action and otherwise.
            state: state after do action.
                   None if inplace is True.
            
        '''
        if action[1] in self.get_possible_moves(state).get(action[0], []):
            return True,self.move(state, action, inplace)
        return False, None


if __name__ == '__main__':
    # Test Space
    game = Problem()
    dictionary = game.get_possible_moves(game.init_state)
    for key, values in dictionary.items():
        print(f"{key}: {values}")
    pass