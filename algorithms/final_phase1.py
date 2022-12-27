import numpy as np
import copy
from collections import deque
import random
MAX_DEPTH = 3


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
        if (not prev_state):
            return None
        prev_player = prev_state.player
        now_player = state.player
        prev_action = None
        now_action = None
        if(prev_player != -now_player):
            raise Exception("Invalid state")
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if ((prev_state.board[coor_y][coor_x] == prev_player) & (state.board[coor_y][coor_x] == 0)):
                    prev_action = (coor_y, coor_x)
                if ((state.board[coor_y][coor_x] != 0) & (prev_state.board[coor_y][coor_x] == 0)):
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
            if state.board[value[0]][value[1]] == 0:
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
        capture_dict = dict({})
        is_cap = False
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if state.board[coor_y][coor_x] == state.player:
                    next_moves = self.can_move(state, (coor_y, coor_x))
                    possible_capture = []
                    for next_move in next_moves:
                        neighbor = self.get_valid_neighbors(state, next_move)
                        flat_coor = next_move[0] * state.width + next_move[1]
                        for pos in neighbor:
                            if pos == (coor_y, coor_x):
                                continue
                            if state.board[pos[0]][pos[1]] == -state.player:
                                flat_pos = pos[0] * state.width + pos[1]
                                opposite_pos = divmod(flat_coor*2 - flat_pos, state.width)
                                if opposite_pos in neighbor:
                                    if state.board[opposite_pos[0]][opposite_pos[1]] == -state.player:
                                        is_cap = True
                                        break
                        if(is_cap):
                            possible_capture.append(next_move)
                    if(is_cap):
                        if (possible_capture):
                            capture_dict[(coor_y, coor_x)] = possible_capture
                    if (next_moves):
                        dictionary[(coor_y, coor_x)] = next_moves
        if (not is_cap):
            return dictionary
        else:
            output_dict = dict({})
            use_open_move = False

            for key, values in capture_dict.items():
                if action[0] in values:
                    use_open_move = True
                    output_dict[key] = [action[0]]
            if (use_open_move):
                return output_dict
            else:
                return capture_dict                

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
        state.board[action[1][0]][action[1][1]] = state.board[action[0][0]][action[0][1]]
        state.board[action[0][0]][action[0][1]] = 0
        capture_list = self.capture(state, action[1])
        for pos in capture_list:
            state.board[pos[0]][pos[1]] = state.player

        q = deque()
        liberty_table = copy.deepcopy(state.board)
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if (state.board[coor_y][coor_x] == 0):
                    q.append((coor_y, coor_x))
                    liberty_table[coor_y][coor_x] = 3

        while (len(q) > 0):
            cur = q.popleft()
            neighbor = self.get_valid_neighbors(state, cur)
            for value in neighbor:
                if liberty_table[value[0]][value[1]] == -state.player:
                    liberty_table[value[0]][value[1]] = 3
                    q.append(value)
        
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if (liberty_table[coor_y][coor_x] == -state.player):
                    state.board[coor_y][coor_x] = state.player        
        state.player *= -1

        if not inplace:
            return state

def move(prev_board, board, player, remain_time_x, remain_time_y):
    '''
        Get random move

        Input
        ----------
            board: map(5*5);
            player: 1 or -1, represent for player
            remain_time_x: Time remain (ms)
            remain_time_y: Time remain (ms)
        Output  
        ----------
            optimize action from all possible action.
            eg. ((1,1),(1,2)).  
    '''
    state = State(board, player)
    if (prev_board):
        prev_state = State(prev_board, -player)
    else:
        prev_state = None
    problem = Problem()
    visited_states = {}

    def _hash_state(state: State):
        hash_value = ''
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                hash_value +=   chr(98+state.board[coor_y][coor_x])
        hash_value += chr(98+state.player)
        return hash_value

    def _is_visited(hased_state, depth):
        return hased_state in visited_states and \
            visited_states[hased_state][0] >= depth

    def _add_visited_state(hased_state, depth, score, action):
        if hased_state not in visited_states:
            visited_states[hased_state] = [depth,score,action]
        elif visited_states[hased_state][0] < depth:
            visited_states[hased_state][0] = depth
            visited_states[hased_state][1] = score
            visited_states[hased_state][2] = action

    def _calculate_score(state: State):
        return np.sum(state.board)
        
    def _minimax(prev_state, state, depth, alpha, beta):
        if(depth == 0):
            return (), _calculate_score(state)

        hased_state = _hash_state(state)

        # Get all possible actions
        dict_possible_moves = problem.get_possible_moves(prev_state, state)
        best_action = None
        best_value  = 0

        if(state.player == 1):
            best_value = -1000
            for start, possible_moves in dict_possible_moves.items():
                for end in possible_moves:
                    next_move = (start, end)
                    next_state = problem.move(state, next_move)
                    hased_next_state = _hash_state(next_state)

                    if(_is_visited(hased_next_state, depth-1)):
                        value = visited_states[hased_next_state][1]
                    else:
                        action, value = _minimax(state, next_state, depth-1, alpha, beta)
                        _add_visited_state(hased_next_state, depth-1, value, action)

                    if value > best_value:
                        best_value = value
                        best_action = next_move
                        
                    if alpha < best_value:
                        alpha = best_value

                    if(beta <= alpha): break
            
        else:
            best_value = 1000
            for start, possible_moves in dict_possible_moves.items():
                for end in possible_moves:
                    next_move = (start, end)
                    next_state = problem.move(state, next_move)
                    hased_next_state = _hash_state(next_state)

                    if(_is_visited(hased_next_state, depth-1)):
                        value = visited_states[hased_next_state][1]
                    else:
                        action, value = _minimax(state, next_state, depth-1, alpha, beta)
                        _add_visited_state(hased_next_state, depth-1, value, action)

                    if value < best_value:
                        best_value = value
                        best_action = next_move

                    if beta > best_value:
                        beta = best_value

                    if(beta <= alpha): break
                
        return best_action, best_value

    action, value = _minimax(prev_state, state, MAX_DEPTH, -1000, 1000)
    return action

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
    testcase1 = {
        "prev_board": [[-1,  0,  -1,  0,  0],
                      [1,  -1,  0,  1,  0],
                      [1,  0,  0,  1, 1],
                      [1,  1,  0,  -1, 1],
                      [0, 1, 1, 1, 1]],
        "board": [[-1,  0,  -1,  0,  0],
                 [1,  0,  0,  1,  0],
                 [1,  0,  -1,  1, 1],
                 [1,  1,  0,  -1, 1],
                 [0, 1, 1, 1, 1]]          
    }
    
    testcase2 = {
        "prev_board": None,
        "board": [[1,  1,  1,  1,  1],
                 [1,  0,  0,  0,  1],
                 [1,  0,  0,  0, -1],
                 [-1,  0,  0,  0, -1],
                 [-1, -1, -1, -1, -1]]        
    }

    testcase3 = {
        "prev_board": [[-1,  0,  0,  0,  0],
                      [1,  -1,  0,  1,  0],
                      [1,  0,  -1,  1, 1],
                      [1,  1,  0,  -1, 1],
                      [0, 1, 1, 1, 1]],
        "board": [[-1,  0,  -1,  0,  0],
                 [1,  0,  0,  1,  0],
                 [1,  0,  -1,  1, 1],
                 [1,  1,  0,  -1, 1],
                 [0, 1, 1, 1, 1]]        
    }

    player = 1
    chosen = int(input("Lựa chọn testcase (1/2/3): "))
    game = Problem()
    if(chosen == 1):
        print_board(testcase1["board"])
        print()
        state = State(testcase1["board"], player)
        if(testcase1["prev_board"]):
            prev_state = State(testcase1["prev_board"], -player)
            print("Nuoc di mo:", game.get_possible_moves(prev_state, state))
        else:
            print("Nuoc di mo:", game.get_possible_moves(None, state))
        print("Lua chon cua ban: ", move(testcase1["prev_board"], testcase1["board"], player, 1, 1))

    if(chosen == 2):
        print_board(testcase2["board"])
        print()
        state = State(testcase2["board"], player)
        if(testcase2["prev_board"]):
            prev_state = State(testcase2["prev_board"], -player)
            print("Nuoc di mo:", game.get_possible_moves(prev_state, state))
        else:
            print("Nuoc di mo:", game.get_possible_moves(None, state))
        print("Lua chon cua ban: ", move(testcase2["prev_board"], testcase2["board"], player, 1, 1))

    if(chosen == 3):
        print_board(testcase3["board"])
        print()
        state = State(testcase3["board"], player)
        if(testcase3["prev_board"]):
            prev_state = State(testcase3["prev_board"], -player)
            print("Nuoc di mo:", game.get_possible_moves(prev_state, state))
        else:
            print("Nuoc di mo:", game.get_possible_moves(None, state))
        print("Lua chon cua ban: ", move(testcase3["prev_board"], testcase3["board"], player, 1, 1))                             