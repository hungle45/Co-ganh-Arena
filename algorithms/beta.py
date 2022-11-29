import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.problem import State, Problem


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
    pass


if __name__ == '__main__':
    pass
