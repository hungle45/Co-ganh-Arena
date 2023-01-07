import os
import time
import random

from tensorflow.keras.models import load_model

from algorithms import Problem,alpha,deep_ai

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
random.seed(45)


def fight(num_match, max_move=50):
    result = {1:0, 0:0, -1:0}
    problem = Problem()
    model = load_model('./ml_algorithms/model/model.h5')

    for i in range(num_match):
        pre_state = None
        cur_state = problem.init_state

        for _ in range(max_move):
            pre_board = pre_state.board if pre_state is not None else None
            
            action = deep_ai(pre_board, cur_state.board, 1, 100, 100, model)
            
            pre_state = cur_state
            cur_state = problem.move(cur_state, action)

            if cur_state.check_winning_state() == 1:
                break
            
            action = alpha(pre_state.board, cur_state.board, -1, 100, 100)
            
            pre_state = cur_state
            cur_state = problem.move(cur_state, action)

            if cur_state.check_winning_state() == -1:
                break
        
        result[cur_state.check_winning_state()] += 1
        
        if cur_state.check_winning_state() == 1:
            print(f'Match {i}: DeepAI Win')
        elif cur_state.check_winning_state() == 0:
            print(f'Match {i}: Draw')
        else:  
            print(f'Match {i}: RandomBot Win')

    
    return result


if __name__ == '__main__':
    result = fight(4)

    print('\n----------------------------------')
    print(f'Win : {result[1]}')
    print(f'Draw: {result[0]}')
    print(f'Loss: {result[-1]}')
