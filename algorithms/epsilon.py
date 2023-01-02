
import numpy as np
import sys
import os
import random
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.problem import State, Problem


'''
    Improve delta with ordering move
'''


MAX_DEPTH = 5

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
    prev_state = State(prev_board, -player) if prev_board is not None else None
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

    def _add_visited_state(hased_state, depth, score):
        if hased_state not in visited_states:
            visited_states[hased_state] = [depth,score]
        elif visited_states[hased_state][0] < depth:
            visited_states[hased_state][0] = depth
            visited_states[hased_state][1] = score

    def _calculate_score(state: State):
        return np.sum(state.board)
        
    def _minimax(prev_state, state, depth, alpha, beta):
        if state.check_winning_state() != 0:
            return (), 1000*state.check_winning_state()

        if(depth == 0):
            return (), _calculate_score(state)

        hased_state = _hash_state(state)

        # Get all possible actions
        dict_possible_moves = problem.get_possible_moves(prev_state, state)

        # Get all possible state and their info (move to get, score)
        next_states_info = []
        for start, possible_ends in dict_possible_moves.items():
            for end in possible_ends:
                next_move = (start, end)
                next_state = problem.move(state, next_move)
                score = _calculate_score(next_state)
                next_states_info.append((score,next_move,next_state))

        best_move = None
        best_score  = 0

        if(state.player == 1):
            next_states_info.sort(key=lambda x: x[0], reverse=True) # sort by score

            best_score = -1000
            for _, next_move, next_state in next_states_info:
                hased_next_state = _hash_state(next_state)

                if(_is_visited(hased_next_state, depth-1)):
                    value = visited_states[hased_next_state][1]
                else:
                    _, value = _minimax(state, next_state, depth-1, alpha, beta)
                    _add_visited_state(hased_next_state, depth-1, value)

                if value > best_score:
                    best_score = value
                    best_move = next_move
                    
                if alpha < best_score:
                    alpha = best_score

                if(beta <= alpha): break
            
        else:
            next_states_info.sort(key=lambda x: x[0], reverse=False) # sort by score

            best_score = 1000
            for _, next_move, next_state in next_states_info:
                hased_next_state = _hash_state(next_state)

                if(_is_visited(hased_next_state, depth-1)):
                    value = visited_states[hased_next_state][1]
                else:
                    _, value = _minimax(state, next_state, depth-1, alpha, beta)
                    _add_visited_state(hased_next_state, depth-1, value)

                if value < best_score:
                    best_score = value
                    best_move = next_move

                if beta > best_score:
                    beta = best_score

                if(beta <= alpha): break

        if best_move is None:
            for start in dict_possible_moves.keys():
                best_move = (start,dict_possible_moves[start][0])
                break

        return best_move, best_score

    action, value = _minimax(prev_state, state, MAX_DEPTH, -1000, 1000)
    return action


if __name__ == '__main__':
    start = time.time()
    prev_board=[[ 0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  1],
                [ 1,  0,  0,  1,  1],
                [ 1,  1,  1,  0, -1]]
    board=[[ 0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  1],
            [ 1,  0,  0,  1,  1],
            [ 1,  1,  1,  0, -1]]
    player = -1
    a = move(prev_board, board, player, 1, 1)
    print(time.time()-start)
    print(a)
