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
            random action from all possible action.
            eg. ((1,1),(1,2)).

    '''
    state = State(board, player)
    problem = Problem()
    dict_possible_moves = problem.get_possible_moves(state)
    all_possible_moves = []

    for position, possible_position_moves in dict_possible_moves.items():
        for possible_move in possible_position_moves:
            all_possible_moves.append((position, possible_move))

    number_possible_moves = len(all_possible_moves)
    random_number = random.randint(0, number_possible_moves)
    return all_possible_moves[random_number]


if __name__ == '__main__':
    board = [[1,  1,  1,  1,  1],
             [1,  0,  0,  0,  1],
             [1,  0,  0,  0, -1],
             [-1,  0,  0,  0, -1],
             [-1, -1, -1, -1, -1]]
    player = 1
    a = move(board, player, 1, 1)
    print(a)
