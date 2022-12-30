import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.problem import State, Problem


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
    prev_state = State(prev_board, -player) if prev_board is not None else None
    problem = Problem()
    dict_possible_moves = problem.get_possible_moves(prev_state, state)
    all_possible_moves = []

    for position, possible_position_moves in dict_possible_moves.items():
        for possible_move in possible_position_moves:
            all_possible_moves.append((position, possible_move))

    # number_possible_moves = len(all_possible_moves)
    # random_number = random.randint(0, number_possible_moves-1)
    # return all_possible_moves[random_number]

    random_move = random.choice(all_possible_moves)
    return random_move


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
    player = 1
    a = move(prev_board, board, player, 5000, 5000)
    print(a)
