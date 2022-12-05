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

    def get_possible_position_and_liberty(self, state: State, pos: tuple):
        '''
        Get all possible moves for given position.

        Input
        ----------
            state: input State.
            pos: current position
            
        Output
        ----------
            possible_move: output dict of possible move with key is the starting 
                           position, value is a list of the destination position.
                           eg. {
                            (1,2): [(2,2),(1,1),...]
                           }
            liberity: output dict of possible liberity with current position
                            eg. {
                            (0, 0): [(0, 1), (1, 0), (1, 1)]
                            }
            
        '''        

        player = state.board[pos]
        position = []
        liberity = []
        coor_y, coor_x = pos

        left_cond = (coor_x > 0)
        right_cond = (coor_x < state.width - 1)
        up_cond = (coor_y > 0)
        down_cond = (coor_y < state.height - 1)

        if left_cond:
            if state.board[coor_y, coor_x - 1] == player:
                liberity.append((coor_y, coor_x - 1))
            if state.board[coor_y, coor_x - 1] == 0:
                liberity.append((coor_y, coor_x - 1))
                position.append((coor_y, coor_x - 1))
                
        if right_cond:
            if state.board[coor_y, coor_x + 1] == player:
                liberity.append((coor_y, coor_x + 1))
            if state.board[coor_y, coor_x + 1] == 0:
                liberity.append((coor_y, coor_x + 1))
                position.append((coor_y, coor_x + 1))
        
        if up_cond:
            if state.board[coor_y - 1, coor_x] == player:
                liberity.append((coor_y - 1, coor_x))
            if state.board[coor_y - 1, coor_x] == 0:
                liberity.append((coor_y - 1, coor_x))
                position.append((coor_y - 1, coor_x))
        
        if down_cond:
            if state.board[coor_y + 1, coor_x] == player:
                liberity.append((coor_y + 1, coor_x))
            if state.board[coor_y + 1, coor_x] == 0:
                liberity.append((coor_y + 1, coor_x))
                position.append((coor_y + 1, coor_x))

        if ((coor_x + coor_y) % 2 == 0):
            top_left_cond = ((coor_y > 0) & (coor_x > 0))
            top_right_cond = ((coor_y > 0) & (coor_x + 1 < state.width))
            bottom_left_cond = ((coor_y + 1 < state.height) & (coor_x > 0))
            bottom_right_cond = ((coor_y + 1 < state.height) & (coor_x + 1 < state.width))
            if top_left_cond:
                if state.board[coor_y - 1, coor_x - 1] == player:
                    liberity.append((coor_y - 1, coor_x - 1))
                if state.board[coor_y - 1, coor_x - 1] == 0:
                    liberity.append((coor_y - 1, coor_x - 1))
                    position.append((coor_y - 1, coor_x - 1))

            if top_right_cond:
                if state.board[coor_y - 1, coor_x + 1] == player:
                    liberity.append((coor_y - 1, coor_x + 1))
                if state.board[coor_y - 1, coor_x + 1] == 0:
                    liberity.append((coor_y - 1, coor_x + 1))
                    position.append((coor_y - 1, coor_x + 1))

            if bottom_left_cond:
                if state.board[coor_y + 1, coor_x - 1] == player:
                    liberity.append((coor_y + 1, coor_x - 1))
                if state.board[coor_y + 1, coor_x - 1] == 0:
                    liberity.append((coor_y + 1, coor_x - 1))
                    position.append((coor_y + 1, coor_x - 1))

            if bottom_right_cond:
                if state.board[coor_y + 1, coor_x + 1] == player:
                    liberity.append((coor_y + 1, coor_x + 1))
                if state.board[coor_y + 1, coor_x + 1] == 0:
                    liberity.append((coor_y + 1, coor_x + 1))
                    position.append((coor_y + 1, coor_x + 1))       
        return position, liberity

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
            return pos[0]*1000 + pos[1]

        dictionary = dict({})
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                if state.board[coor_y, coor_x] == state.player:
                    position, _ = self.get_possible_position_and_liberty(state, (coor_y, coor_x))

                    if (position):
                        dictionary[(coor_y, coor_x)] = sorted(position, key= compare_pos)
        return dictionary    
               
    def is_liberty(self, state: State, pos: tuple):
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
        q.append(pos)

        def define_value():
            return False

        visited = defaultdict(define_value)

        def _is_visited(pos: tuple):
            nonlocal visited
            return visited[pos]
        
        def _add_visited_pos(pos: tuple):
            nonlocal visited
            visited[pos] = True
        _add_visited_pos(pos= pos)
        while (len(q) > 0):
            cur = q.popleft()
            _, liberity_list = self.get_possible_position_and_liberty(state, cur)
            for ally in liberity_list:
                if _is_visited(ally):
                    continue

                if state.board[ally] == 0:
                    return True, None
                
                _add_visited_pos(ally)
                q.append(ally)
        return False, visited
    
    def capture(self, state: State, pos_action: tuple):
        player = state.board[pos_action]
        coor_y, coor_x = pos_action
        
        capture_list = []

        left_cond = (coor_x > 0)
        right_cond = (coor_x < state.width - 1)
        up_cond = (coor_y > 0)
        down_cond = (coor_y < state.height - 1)
        is_left_append, is_right_append, is_up_append, is_down_append = False, False, False, False

        if left_cond and right_cond:
            left_pos = state.board[coor_y, coor_x - 1]
            right_pos = state.board[coor_y, coor_x + 1]
            if ((left_pos == right_pos) & (left_pos == -player)):
                if not is_left_append:
                    capture_list.append((coor_y, coor_x - 1))
                    is_left_append = True

                if not is_right_append:
                    capture_list.append((coor_y, coor_x + 1))
                    is_right_append = True

        if up_cond and down_cond:
            up_pos = state.board[coor_y - 1, coor_x]
            down_pos = state.board[coor_y + 1, coor_x]
            if ((up_pos == down_pos) & (up_pos == -player)):
                if not is_up_append:
                    capture_list.append((coor_y - 1, coor_x))
                    is_up_append = True

                if not is_down_append:
                    capture_list.append((coor_y + 1, coor_x))
                    is_down_append = True

        if ((coor_x + coor_y) % 2 == 0):
            top_left_cond = ((coor_y > 0) & (coor_x > 0))
            top_right_cond = ((coor_y > 0) & (coor_x + 1 < state.width))
            bottom_left_cond = ((coor_y + 1 < state.height) & (coor_x > 0))
            bottom_right_cond = ((coor_y + 1 < state.height) & (coor_x + 1 < state.width))
            is_top_left_append, is_top_right_append, is_bottom_left_append, is_bottom_right_append = False, False, False, False             

            if top_left_cond and bottom_right_cond:
                top_left_pos = state.board[coor_y - 1, coor_x - 1]
                bottom_right_pos = state.board[coor_y + 1, coor_x + 1]
                if((top_left_pos == bottom_right_pos) & (top_left_pos == -player)):
                    if not is_top_left_append:
                        capture_list.append((coor_y - 1, coor_x - 1))
                        is_top_left_append = True        

                    if not is_bottom_right_append:
                        capture_list.append((coor_y + 1, coor_x + 1))
                        is_bottom_right_append = True                                   

            if top_right_cond and bottom_left_cond:
                top_right_pos = state.board[coor_y - 1, coor_x + 1]
                bottom_left_pos = state.board[coor_y + 1, coor_x - 1]
                if((top_right_pos == bottom_left_pos) & (top_right_pos == -player)):
                    if not is_top_right_append:
                        capture_list.append((coor_y - 1, coor_x + 1))
                        is_top_right_append = True 

                    if not is_bottom_left_append:
                        capture_list.append((coor_y + 1, coor_x - 1))
                        is_bottom_left_append = True
        return capture_list

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

        for pos_y in range(state.height):
            for pos_x in range(state.width):
                if(state.board[pos_y, pos_x] == -state.player):
                    check_liberty, visited = self.is_liberty(state, (pos_y, pos_x))
                    # print(check_liberty)
                    # print(visited)
                    if not check_liberty:
                        print(list(visited))

                        for position, _ in visited.items():
                            state.board[position] = state.player
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
    for pos_y in range(game.init_state.height):
        for pos_x in range(game.init_state.width):
            if game.init_state.board[pos_y, pos_x] == game.init_state.player:
                _, liberty_pos = game.get_possible_position_and_liberty(game.init_state, (pos_y, pos_x))
                result = game.is_liberty(game.init_state, (pos_y, pos_x))
                print(result[0])
                print(f"({pos_y},{pos_x}): {liberty_pos}")