import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.problem import State, Problem

def hash_state(state: State):
    hash_value = ''
    for coor_y in range(state.height):
        for coor_x in range(state.width):
            hash_value += chr(98+state.board[coor_y][coor_x])
    hash_value += chr(98+state.player)
    return hash_value


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
        totalPoint = 0
        for coor_y in range(state.height):
            for coor_x in range(state.width):
                totalPoint += state.board[coor_y][coor_x]
        return totalPoint

    def minimax(state, depth, alpha, beta):
        if(depth == 0):
            return calculatePoint(state)
        problem = Problem()

        _add_visited_state(state)
        # Get all possible actions
        dict_possible_moves = problem.get_possible_moves(state)
        all_possible_moves = []
        for position, possible_position_moves in dict_possible_moves.items():
            for possible_move in possible_position_moves:
                all_possible_moves.append((position, possible_move))

        if(state.player == 1):
            maxPoint = -1000
            for possible_move in all_possible_moves:
                next_state = problem.move(state, possible_move)
                if(_is_visited(next_state)):
                    continue
                point = minimax(next_state, depth-1, alpha, beta)
                maxPoint = max(maxPoint, point)
                alpha = max(alpha, maxPoint)
                if(beta <= alpha):
                    break
            return maxPoint
        else:
            minPoint = 1000
            for possible_move in all_possible_moves:
                next_state = problem.move(state, possible_move)
                if(_is_visited(next_state)):
                    continue
                point = minimax(next_state, depth-1, alpha, beta)
                minPoint = min(minPoint, point)
                beta = min(beta, minPoint)
                if(beta <= alpha):
                    break
            return minPoint

    state = State(board, player)
    a = minimax(state, 8, -1000, 1000)
    print(a)


if __name__ == '__main__':
    board = [[1,  1,  1,  1,  1],
             [1,  0,  0,  0,  1],
             [1,  0,  0,  0, -1],
             [-1,  0,  0,  0, -1],
             [-1, -1, -1, -1, -1]]
    player = 1
    move(board, player, 1, 1)
