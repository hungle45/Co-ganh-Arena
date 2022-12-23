import numpy as np
import random


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
                if ((prev_state.board[coor_y, coor_x] == prev_player) & (state.board[coor_y, coor_x] == 0)):
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
                if state.board[coor_y, coor_x] == state.player:
                    next_moves = self.can_move(state, (coor_y, coor_x))
                    possible_capture = []
                    for next_move in next_moves:
                        neighbor = self.get_valid_neighbors(state, next_move)
                        flat_coor = next_move[0] * state.width + next_move[1]
                        for pos in neighbor:
                            if pos == (coor_y, coor_x):
                                continue
                            if state.board[pos] == -state.player:
                                flat_pos = pos[0] * state.width + pos[1]
                                opposite_pos = divmod(flat_coor*2 - flat_pos, state.width)
                                if opposite_pos in neighbor:
                                    if state.board[opposite_pos] == -state.player:
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
            random action from all possible action.
            eg. ((1,1),(1,2)).  

    '''

    state = State(board, player)
    if (prev_board):
        prev_state = State(prev_board, -player)
    else:
        prev_state = None
    problem = Problem()
    dict_possible_moves = problem.get_possible_moves(prev_state, state)
    all_possible_moves = []

    for position, possible_position_moves in dict_possible_moves.items():
        for possible_move in possible_position_moves:
            all_possible_moves.append((position, possible_move))

    random_move = random.choice(all_possible_moves)
    return random_move

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