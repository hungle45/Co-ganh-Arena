import numpy as np

class State:
    def __init__(self, board: list, player: int):
        self.player = player
        self.board = np.array(board)

    def __eq__(self, other):
        return np.array_equal(self.board,other.board) \
            and self.player == other.player


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

    def move(self, state:State, action, inplace=False):
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

        if action[1] in self.get_possible_moves(state)[action[0]]:
            return True,self.move(state, action, inplace)
        return False,None


if __name__ == '__main__':
    # Test Space
    pass