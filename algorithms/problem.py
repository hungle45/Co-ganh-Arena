from collections import deque, defaultdict
import copy
import time

import numpy as np

def _move_AI_bounder(board, player, remain_time_x, remain_time_y,algorithm,return_queue):
    # move = algorithm(board, player, remain_time_x, remain_time_y)
    start_time = time.time()
    move = algorithm(board, player, remain_time_x, remain_time_y)
    end_time = time.time()
    return_queue.put((move,(end_time-start_time)*1000))

class State:
    def __init__(self, board: list, player: int):
        self.player = player
        self.flatten_board = np.array(self._flatten_state(np.array(board)))
        self.board = np.array(board)
        self.height = np.array(board).shape[0]
        self.width = np.array(board).shape[1]

    def _flatten_state(self, board):
        res_board = []
        for coor_y in range(board.shape[0]):
            for coor_x in range(board.shape[1]):
                res_board.append(board[coor_y, coor_x])
        return res_board

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

    def flatten(self, state: State, coor):
        return state.width*coor[0] + coor[1]
    
    def unflatten(self, state: State, flat_coor):
        return divmod(flat_coor, state.width)
    
    def is_on_board(self, state: State, coor):
        return coor[0] % state.height == coor[0] \
            and coor[1] % state.width == coor[1]

    def get_valid_neighbors(self, state: State, flat_coor):
        coor_y, coor_x = self.unflatten(state, flat_coor)
        possible_neighbors = ((coor_y + 1, coor_x), (coor_y - 1, coor_x), (coor_y, coor_x + 1), (coor_y, coor_x - 1))
        if ((coor_x + coor_y) % 2 == 0):
            possible_neighbors += ((coor_y + 1, coor_x + 1), (coor_y - 1, coor_x + 1), (coor_y + 1, coor_x - 1), (coor_y - 1, coor_x - 1))
        return sorted([self.flatten(state, coor) for coor in possible_neighbors if self.is_on_board(state, coor)])

    def can_move(self, state: State, flat_coor):
        neighbor = self.get_valid_neighbors(state, flat_coor)
        mask = np.where(state.flatten_board[neighbor] == 0)
        return np.array(neighbor)[mask]

    def share_liberty(self, state: State, flat_coor):
        neighbor = self.get_valid_neighbors(state, flat_coor)
        mask = np.where(state.flatten_board[neighbor] != -state.flatten_board[flat_coor])
        return np.array(neighbor)[mask]
    
    def is_liberty(self, state: State, flat_coor):
        '''
        Checking if current position has liberty

        Input
        ----------
            state: input State.
            pos: position which need check liberty
            
        Output
        ----------
            True if current position have liberty and otherwise
            visited: All position share liberty with current position
        '''        
        q = deque()
        q.append(flat_coor)

        def define_value():
            return False

        visited = defaultdict(define_value)

        def _is_visited(flat_coor):
            nonlocal visited
            return visited[flat_coor]
        
        def _add_visited_pos(flat_coor):
            nonlocal visited
            visited[flat_coor] = True
        
        _add_visited_pos(flat_coor= flat_coor)
        while (len(q) > 0):
            cur = q.popleft()
            liberty_list = self.share_liberty(state, cur)
            for ally in liberty_list:
                if _is_visited(ally):
                    continue

                if state.flatten_board[ally] == 0:
                    return True, None
                
                _add_visited_pos(ally)
                q.append(ally)
        return False, visited

    def get_possible_moves(self, state: State):
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
        dictionary = dict({})
        dictionary_capture = dict({})
        is_capture = False

        for i in range(state.height * state.width):
            if state.flatten_board[i] == state.player:
                can_move_list = self.can_move(state, i)
                capture_move = []
                for move in can_move_list:
                    check_state = copy.deepcopy(state)
                    check_state.flatten_board[move] = check_state.flatten_board[i]
                    check_state.flatten_board[i] = 0
                    if (self.capture(check_state, move)):
                        is_capture = True
                        capture_move.append(move)   
                if (is_capture):
                    if capture_move:
                        dictionary_capture[self.unflatten(state, i)] = [self.unflatten(state, pos) for pos in capture_move]                
                else:
                    if list(can_move_list):
                        dictionary[self.unflatten(state, i)] = [self.unflatten(state, pos) for pos in self.can_move(state, i)]
        if is_capture:
            return dictionary_capture
        else: 
            return dictionary  

    def capture(self, state: State, flat_coor):
        player = state.flatten_board[flat_coor]
        capture_list = set()
        neighbor = self.get_valid_neighbors(state, flat_coor)
        for pos in neighbor:
            if state.flatten_board[pos] == -player:
                if (flat_coor*2 - pos) in neighbor:
                    if state.flatten_board[flat_coor*2 - pos] == -player:
                        capture_list.add(pos)
        return list(capture_list)


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
        before, after = self.flatten(state, action[0]), self.flatten(state, action[1])

        state.flatten_board[after] = state.flatten_board[before]
        state.flatten_board[before] = 0
        capture_list = self.capture(state, after)
        for pos in capture_list:
            state.flatten_board[pos] = state.player
        
        for fc in range(state.height * state.width):
            if(state.flatten_board[fc] == -state.player):
                check_liberty, visited = self.is_liberty(state, fc)
                if not check_liberty:
                    for position, _ in visited.items():
                        state.flatten_board[position] = state.player 

        for fc in range(state.height * state.width):
            state.board[divmod(fc, state.width)] = state.flatten_board[fc]
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
    for fc in range(game.init_state.height * game.init_state.width):
        if game.init_state.flatten_board[fc] == game.init_state.player:
            liberty_pos = game.share_liberty(game.init_state, fc)
            result = game.is_liberty(game.init_state, fc)
            print(result[0])
            pos_y, pos_x = divmod(fc, game.init_state.width)
            print(f"({pos_y},{pos_x}): {[divmod(pos, game.init_state.width) for pos in liberty_pos]}")