import sys, os, random
from collections import deque

from tqdm import tqdm
import numpy as np
# import torch
# from torch.utils.data import Dataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from algorithms import State, Problem


PROBLEM = Problem()


def random_board(depth_range=(5,95)):
    '''
    Get random board, only in X(1) player's turn

    Output
        ----------
        return board: a numpy array size (4,5,5) with
            channel 0: zero-one array for O(-1) player's pieces in cur_board
            channel 1: zero-one array for X( 1) player's pieces in cur_board
            channel 2: zero-one array for O(-1) player's pieces in pre_board
            channel 3: zero-one array for X( 1) player's pieces in pre_board
    '''
    pre_state = None
    cur_state = PROBLEM.init_state
    depth = random.randrange(*depth_range)

    for _ in range(depth):
        dict_possible_moves = PROBLEM.get_possible_moves(pre_state, cur_state)
        all_possible_moves = []

        for start, possible_moves in dict_possible_moves.items():
            for end in possible_moves:
                all_possible_moves.append((start, end))
        
        random_move = random.choice(all_possible_moves)
        
        next_state = PROBLEM.move(cur_state, random_move)
        if next_state.check_winning_state() != 0: break
        
        pre_state = cur_state
        cur_state = next_state

    # print(pre_state)
    # print(cur_state)
    
    board = np.zeros((4,5,5))

    if cur_state.player == 1:
        board[0] = (cur_state.board == -1).astype(np.float32)
        board[1] = (cur_state.board == 1).astype(np.float32)
        board[2] = (pre_state.board == -1).astype(np.float32)
        board[3] = (pre_state.board == 1).astype(np.float32)

    else:
        board[0] = (cur_state.board == 1).astype(np.float32)
        board[1] = (cur_state.board == -1).astype(np.float32)
        board[2] = (pre_state.board == 1).astype(np.float32)
        board[3] = (pre_state.board == -1).astype(np.float32)
    
    return board
        


def generate_dataset(path, sample_per_depth, depth_range=(5,95)):
    pass


def analyze_state(max_depth=5):
    '''
    Use this funtion have a glance view on all possible state (only consider cur_state, not including pre_state)
    '''
    init_state = PROBLEM.init_state

    state_set = {init_state}
    
    q = deque([(None,init_state)])
    print(f'Depth 0 has {len(state_set)} state')
    
    for depth in range(1,max_depth):
        last_num = len(q)
        for _ in range(last_num):
            prev_state, cur_state = q.popleft()

            if cur_state.check_winning_state() != 0:
                continue

            dict_possible_moves = PROBLEM.get_possible_moves(prev_state, cur_state)

            for start, possible_moves in dict_possible_moves.items():
                for end in possible_moves:
                    next_state = PROBLEM.move(cur_state, (start,end))

                    if next_state in state_set:
                        continue

                    q.append((cur_state,next_state))
                    state_set.add(next_state)
            
        print(f'Depth {depth} has {len(state_set)} states')

    return True


class BoardDataset(Dataset):
    pass


if __name__ == '__main__':
    print(random_board())