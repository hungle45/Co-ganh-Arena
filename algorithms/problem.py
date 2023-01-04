from collections import deque
import copy
import time

import numpy as np

def _move_AI_bounder(prev_board, board, player, remain_time_x, remain_time_y,algorithm,return_queue):
    # move = algorithm(board, player, remain_time_x, remain_time_y)
    start_time = time.time()
    move = algorithm(prev_board, board, player, remain_time_x, remain_time_y)
    end_time = time.time()
    return_queue.put((move,(end_time-start_time)*1000))


class State:
    def __init__(self, board: list, player: int):
        self.player = player
        self.board = np.array(board)
        self.height = self.board.shape[0]
        self.width = self.board.shape[1]

    def __eq__(self, other):
        return np.array_equal(self.board,other.board) \
            and self.player == other.player

    def __str__(self):
        str_board = '\n       '.join(str(self.board).split('\n'))
        str_board = str_board.replace('-1', ' O')
        str_board = str_board.replace('1', 'X')
        str_board = str_board.replace('0', '+')

        str_player = 'X' if self.player == 1 else 'O' 

        return f'Board: {str_board}\nPlayer\'s turn: {str_player}'
    
    def __hash__(self):
        hash_value = ''
        for coor_y in range(self.height):
            for coor_x in range(self.width):
                hash_value +=   chr(98+self.board[coor_y][coor_x])
        hash_value += chr(98+self.player)
        return hash(hash_value)

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

    def get_open_move(self, prev_state:State, state:State):
        '''Get open move for given state
        Input: 
        ----------
            prev_state: state before returning now state
            state: input State.

        Output
        ----------
            open_move: (prev_action, now_action) Prev_board ---> Present board
            return None if no exist (Never occur unless state is INIT STATE) and otherwise
        '''
        if (prev_state is None):
            return None
        prev_player = prev_state.player
        now_player = state.player
        prev_action = None
        now_action = None
        if(prev_player != -now_player):
            raise Exception("Invalid state")
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if ((prev_state.board[coor_y, coor_x] != 0) & (state.board[coor_y, coor_x] == 0)):
                    prev_action = (coor_y, coor_x)
                if ((state.board[coor_y, coor_x] != 0) & (prev_state.board[coor_y, coor_x] == 0)):
                    now_action = (coor_y, coor_x)
        return (prev_action, now_action)
    
    def is_on_board(self, state: State, coor):
        return coor[0] % state.height == coor[0] \
            and coor[1] % state.width == coor[1]

    def get_valid_neighbors(self, state: State, pos: tuple):
        coor_y, coor_x = pos
        possible_neighbors = ((coor_y + 1, coor_x), (coor_y - 1, coor_x), (coor_y, coor_x + 1), (coor_y, coor_x - 1))
        if ((coor_x + coor_y) % 2 == 0):
            possible_neighbors += ((coor_y + 1, coor_x + 1), (coor_y - 1, coor_x + 1), (coor_y + 1, coor_x - 1), (coor_y - 1, coor_x - 1))
        return [coor for coor in possible_neighbors if self.is_on_board(state, coor)]        

    def can_move(self, state: State, pos: tuple):
        neighbor = self.get_valid_neighbors(state, pos)
        can_move_list = []
        for value in neighbor:
            if state.board[value] == 0:
                can_move_list.append(value)
        return can_move_list 

    def capture(self, state: State, pos_action: tuple):
        player = state.board[pos_action[0]][pos_action[1]]
        coor_y, coor_x = pos_action
        capture_list = []
        flat_coor = coor_y * state.width + coor_x
        neighbor = self.get_valid_neighbors(state, pos_action)
        for pos in neighbor:
            flat_pos = pos[0] * state.width + pos[1]
            if state.board[pos[0]][pos[1]] == -player:
                opposite_pos = divmod(flat_coor*2 - flat_pos, state.width)
                if opposite_pos in neighbor:
                    if state.board[opposite_pos[0]][opposite_pos[1]] == -player:
                        capture_list.append(pos)
        return capture_list                

    def get_possible_moves(self, prev_state: State, state:State):
        '''
        Get all possible moves for given state.

        Input
        ----------
            prev_state: state before returning now state
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
        action = self.get_open_move(prev_state, state)
        dictionary = dict({})
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if state.board[coor_y, coor_x] == state.player:
                    next_moves = self.can_move(state, (coor_y, coor_x))
                    if (len(next_moves)):
                        dictionary[(coor_y, coor_x)] = next_moves
        trap_move = dict({})
        if action is not None:
            # print(f"Action {action[0]} --> {action[1]}")
            neighbor = self.get_valid_neighbors(state, action[0])
            for value in neighbor:
                if state.board[value] == state.player:
                    is_cap = False
                    flat_player = action[0][0] * state.width + action[0][1]
                    for pos in neighbor:
                        if pos == value:
                            continue
                        if state.board[pos] == -state.player:
                            flat_pos = pos[0] * state.width + pos[1]
                            opposite_pos = divmod(flat_player * 2 - flat_pos, state.width)
                            if opposite_pos in neighbor:
                                if state.board[opposite_pos] == -state.player:
                                    is_cap = True
                                    break
                    if is_cap:
                        trap_move[value] = [action[0]]
            if (len(trap_move) == 0):
                return dictionary
            else:
                return trap_move
        else:
            return dictionary

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
        capture_list = self.capture(state, action[1])
        for pos in capture_list:
            state.board[pos] = state.player

        q = deque()
        liberty_table = copy.deepcopy(state.board)
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if (state.board[coor_y, coor_x] == 0):
                    q.append((coor_y, coor_x))
                    liberty_table[coor_y, coor_x] = 3

        while (len(q) > 0):
            cur = q.popleft()
            neighbor = self.get_valid_neighbors(state, cur)
            for value in neighbor:
                if liberty_table[value] == -state.player:
                    liberty_table[value] = 3
                    q.append(value)
        
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if (liberty_table[coor_y, coor_x] == -state.player):
                    state.board[coor_y, coor_x] = state.player        
        state.player *= -1

        if not inplace:
            return state

    def move_if_possible(self, prev_state:State, state:State, action, inplace=False):
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
        if action[1] in self.get_possible_moves(prev_state, state).get(action[0], []):
            return True,self.move(state, action, inplace)
        return False, None

def print_board(board: list):
    height = len(board)
    width = len(board[0])
    for coor_y in range(height-1, -1, -1):
        row = ""
        for coor_x in range(width):
            if (board[coor_y][coor_x] == 1):
                row += "X "
            elif (board[coor_y][coor_x] == -1):
                row += "O "
            else:
                row += "- "
        print(row)
        
if __name__ == '__main__':
    # Test Space
    testcase = {
        "prev_board": [[-1, 0, -1, 1, 1],
                      [-1, -1, 0, 0, 1],
                      [-1, 0, 1, 0, 1],
                      [1, 1, 0, 0, 1],
                      [1, 1, 0, 0, 1]],
        "board": [[-1, 0,  0,  1,  -1],
                  [-1, -1,  0,  -1,  1],
                  [-1, 0,  -1,  0, 1],
                  [1, 1,  0,  0, 1],
                  [1, 1, 0, 0, 1]]      
    }

    # testcase = {
    #     "prev_board": [[ 1,  0,  1, -1, -1],
    #                    [ 1,  1,  0,  0, -1],
    #                    [ 1,  0, -1,  0, -1],
    #                    [-1, -1,  0,  0, -1],
    #                    [-1, -1,  0,  0, -1]],
    #     "board": [[ 1,  0,  0, -1,  1],
    #               [ 1,  1,  0,  1, -1],
    #               [ 1,  0,  1,  0, -1],
    #               [-1, -1,  0,  0, -1],
    #               [-1, -1,  0,  0,  1]]      
    # }

    player = 1
    game = Problem()
    print_board(testcase["board"])
    print()
    state = State(testcase["board"], player)
    if(testcase["prev_board"]):
        prev_state = State(testcase["prev_board"], -player)
        # print("Nuoc di mo:", game.get_possible_moves(prev_state, state))
        print(game.get_open_move(prev_state, state))
    else:
        print("Nuoc di mo:", game.get_possible_moves(None, state))
