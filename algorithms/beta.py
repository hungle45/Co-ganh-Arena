
from algorithms.problem import State, Problem
import numpy as np
import sys
import os
import random
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def hash_state(state: State):
    hash_value = 1 << 31
    for coor_y in range(state.height):
        for coor_x in range(state.width):
            hash_value = hash_value << 2 | (2+state.board[coor_y][coor_x])
    hash_value = hash_value << 2 | (2+state.player)
    return hash_value


def minimax(state, depth, alpha, beta):
    _visitied_states = set()

    def _is_visited(state: State):
        nonlocal _visitied_states
        if(hash_state(state) in _visitied_states):
            return True
        else:
            return False

    def _add_visited_state(state: State):
        nonlocal _visitied_states
        _visitied_states.add(hash_state(state))

    def calculatePoint(state: State):
        return np.sum(state.board)

    if(depth == 0):
        return (), calculatePoint(state)
    problem = Problem()

    _add_visited_state(state)
    # Get all possible actions
    dict_possible_moves = problem.get_possible_moves(state)
    bestAction = ()

    if(state.player == 1):
        max_value = -1000
        for start, possible_moves in dict_possible_moves.items():
            for end in possible_moves:
                next_state = problem.move(state, (start, end))
                if(_is_visited(next_state)):
                    continue
                action, value = minimax(next_state, depth-1, alpha, beta)
                if value > max_value:
                    max_value = value
                    bestAction = (start, end)
                alpha = max(alpha, max_value)
                if(beta <= alpha):
                    break
        return bestAction, max_value
    else:
        min_value = 1000
        for start, possible_moves in dict_possible_moves.items():
            for end in possible_moves:
                next_state = problem.move(state, (start, end))
                if(_is_visited(next_state)):
                    continue
                action, value = minimax(next_state, depth-1, alpha, beta)
                if value < min_value:
                    min_value = value
                    bestAction = (start, end)
                beta = min(beta, min_value)
                if(beta <= alpha):
                    break
        return bestAction, min_value


def move(board, player, remain_time_x, remain_time_y):
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
    problem = Problem()
    action, value = minimax(state, 5, -1000, 1000)
    return action


if __name__ == '__main__':
    start = time.time()
    board = [[-1,  1,  1,  1,  1],
             [1,  0,  0,  0,  1],
             [1,  0,  0,  0, 1],
             [-1,  0,  0,  0, -1],
             [1, 1, 1, 1, 1]]
    player = 1
    state = State(board, player)
    hash_state(state)
    print(1)
    a = move(board, player, 1, 1)
    print(time.time()-start)
