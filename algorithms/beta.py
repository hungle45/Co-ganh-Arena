import random
from problem import State, Problem
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def move(board, player, remain_time_x, remain_time_y):
    '''
        Get random move

        Input
        ----------
            board: map(5*5);
            player: 1 or -1, represent for player
            remain_time_x: Time remain
            remain_time_y: Time remain
        Output
        ----------
            optimize action from all possible action.
            eg. ((1,1),(1,2)).  

    '''

    def minimax(state, depth, alpha, beta):
        if(depth == 0):
            return state.check_winning_state()
        problem = Problem()

        dict_possible_moves = problem.get_possible_moves(state)
        all_possible_moves = []

        for position, possible_position_moves in dict_possible_moves.items():
            for possible_move in possible_position_moves:
                all_possible_moves.append((position, possible_move))

        if(state.player == 1):
            maxPoint = -1
            for possible_move in all_possible_moves:
                next_state = problem.move(state, possible_move)
                point = minimax(next_state, depth-1, alpha, beta)
                maxPoint = max(maxPoint, point)
                alpha = max(alpha, maxPoint)
                if(beta <= alpha):
                    break
            return maxPoint
        else:
            minPoint = 1
            for possible_move in all_possible_moves:
                next_state = problem.move(state, possible_move)
                point = minimax(next_state, depth-1, alpha, beta)
                minPoint = min(minPoint, point)
                beta = min(alpha, minPoint)
                if(beta <= alpha):
                    minPoint
            return minPoint

    # state = State(board, player)
    # a = minimax(state, 1, -1, 1)
    # print(a)


if __name__ == '__main__':
    board = [[1,  1,  1,  1,  1],
             [1,  0,  0,  0,  1],
             [1,  0,  0,  0, -1],
             [-1,  0,  0,  0, -1],
             [-1, -1, -1, -1, -1]]
    player = 1
    a = move(board, player, 1, 1)
