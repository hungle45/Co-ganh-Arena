import sys, os, random, shutil
from collections import deque

from tqdm import tqdm
import numpy as np
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from algorithms import State, Problem, epsilon


PROBLEM = Problem()


def get_random_board(depth_range=(5,95), get_state=False):
    '''
    Get random board, only in X(1) player's turn

    Output
    ----------
        board: a numpy array size (4,5,5) with
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
    
    if get_state:
        return board, pre_state, cur_state
    return board


def get_score(pre_state: State, cur_state: State):
    '''
        Get score of given state, depend on minimax with DEPTH

        Output  
        ----------
            score (int): score evaluated by epsilon with MAX_DEPTH
    '''
    MAX_DEPTH = 5
    visited_states = {}

    def _is_visited(state, depth):
        return state in visited_states and \
            visited_states[state][0] >= depth

    def _add_visited_state(state, depth, score):
        if state not in visited_states:
            visited_states[state] = [depth,score]
        elif visited_states[state][0] < depth:
            visited_states[state][0] = depth
            visited_states[state][1] = score

    def _calculate_score(state: State):
        return np.sum(state.board)
        
    def _minimax(pre_state, cur_state, depth, alpha, beta):
        if cur_state.check_winning_state() != 0:
            return 16*cur_state.check_winning_state()

        if(depth == 0):
            return _calculate_score(cur_state)

        # Get all possible actions
        dict_possible_moves = PROBLEM.get_possible_moves(pre_state, cur_state)

        # Get all possible state and their info (move to get, score)
        next_states_info = []
        for start, possible_ends in dict_possible_moves.items():
            for end in possible_ends:
                next_state = PROBLEM.move(cur_state, (start, end))
                score = _calculate_score(next_state)
                next_states_info.append((score,next_state))

        best_score  = 0

        if(cur_state.player == 1):
            next_states_info.sort(key=lambda x: x[0], reverse=True) # sort by score

            best_score = -16
            for _, next_state in next_states_info:
                if(_is_visited(next_state, depth-1)):
                    value = visited_states[next_state][1]
                else:
                    value = _minimax(cur_state, next_state, depth-1, alpha, beta)
                    _add_visited_state(next_state, depth-1, value)

                if value > best_score:
                    best_score = value
                    
                if alpha < best_score:
                    alpha = best_score

                if(beta <= alpha): break
            
        else:
            next_states_info.sort(key=lambda x: x[0], reverse=False) # sort by score

            best_score = 16
            for _, next_state in next_states_info:
                if(_is_visited(next_state, depth-1)):
                    value = visited_states[next_state][1]
                else:
                    value = _minimax(cur_state, next_state, depth-1, alpha, beta)
                    _add_visited_state(next_state, depth-1, value)

                if value < best_score:
                    best_score = value

                if beta > best_score:
                    beta = best_score

                if(beta <= alpha): break

        return best_score

    return _minimax(pre_state, cur_state, MAX_DEPTH, -16, 16)


def generate_dataset(path, sample_num, depth_range=(5,95), random_state=45):
    '''
        Generate `sample_num` data samples (accept duplicate sample) and save in `path`
        with the following file structure:

            path/
            ├── boards.npy
            └── scores.npy
            
    '''

    random.seed(random_state)
    np.random.seed(random_state)

    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    boards = []
    scores = []
    for _ in tqdm(range(sample_num)):
        b, pre_state, cur_state = get_random_board(depth_range, get_state=True)
        s = get_score(pre_state, cur_state)

        boards.append(b)
        scores.append((s+16)/32)

    boards = np.asarray(boards)
    scores = np.asarray(scores)

    np.save(os.path.join(path,'boards.npy'), boards)
    np.save(os.path.join(path,'scores.npy'), scores)


def analyze_state(max_depth=5):
    '''
        Use this funtion have a glance view on all possible state 
        (only consider cur_state, not including pre_state).
    '''
    init_state = PROBLEM.init_state

    state_set = {init_state}
    
    q = deque([(None,init_state)])
    print(f'Depth 0 has {len(state_set)} state')
    
    for depth in range(1,max_depth):
        last_num = len(q)
        for _ in range(last_num):
            pre_state, cur_state = q.popleft()

            if cur_state.check_winning_state() != 0:
                continue

            dict_possible_moves = PROBLEM.get_possible_moves(pre_state, cur_state)

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
    ''' How to use dataloader

        train_data = BoardDataset(data_path,train=True)
        test_data  = BoardDataset(data_path,train=False)

        train_dataloader = DataLoader(
            dataset=train_data,
            batch_size=BATCH_SIZE,
            shuffle=True
        )

        test_dataloader = DataLoader(
            dataset=test_data,
            batch_size=BATCH_SIZE,
            shuffle=True
        )

    '''
    def __init__(self, root_path, train=True, test_size=0.1, random_state=45):
        boards = np.load(os.path.join(data_path,'boards.npy'))
        scores = np.load(os.path.join(data_path,'scores.npy'))

        boards_train, boards_test, scores_train, scores_test = train_test_split(
            boards, scores, test_size=test_size, random_state=random_state)
        
        self.boards = boards_train if train else boards_test
        self.scores = scores_train if train else scores_test

    def __len__(self):
        return self.boards.shape[0]

    def __getitem__(self, index):
        board = torch.as_tensor(self.boards[index],dtype=torch.float32)
        score = torch.as_tensor(self.scores[index],dtype=torch.float32)

        return board, score


if __name__ == '__main__':
    data_path = 'ds/1000/'
    # generate_dataset(data_path, 1000)