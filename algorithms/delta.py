
import numpy as np
import sys
import os
import random
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.problem import State, Problem


'''
    Improve ability see the future by save the lowest search at each state
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
        if state.check_winning_state() != 0:
            return (), 1000*state.check_winning_state()

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

        if best_action is None:
            for start in dict_possible_moves.keys():
                best_action = (start,dict_possible_moves[start][0])
                break

        return best_action, best_value

    action, value = _minimax(prev_state, state, MAX_DEPTH, -1000, 1000)
    return action


if __name__ == '__main__':
    prev_board = [[-1, 0, -1, 1, 1],
                    [-1, -1, 0, 0, 1],
                    [-1, 0, 1, 0, 1],
                    [1, 1, 0, 0, 1],
                    [1, 1, 0, 0, 1]]
    board = [[-1, 0,  0,  1,  -1],
                [-1, -1,  0,  -1,  1],
                [-1, 0,  -1,  0, 1],
                [1, 1,  0,  0, 1],
                [1, 1, 0, 0, 1]]      
    player = -1
    a = move(prev_board, board, player, 5000, 5000)
    print(a)
