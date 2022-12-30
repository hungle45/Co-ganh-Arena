# ref: https://ai-boson.github.io/mcts/

import sys
import os
import random
import time
from collections import defaultdict
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from algorithms.problem import State, Problem

MAX_DEPTH = 7
TIME_THINKING = 2.8

class MCTSNode:
    def __init__(self, prev_state, state: State, problem, parent=None, parent_action=None):
        self.state = state
        self.prev_state = prev_state
        self.parent = parent
        self.parent_action = parent_action

        self.children = []
        self._number_of_visits = 0

        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0

        self._untried_actions = []
        for start, possible_moves in problem.get_possible_moves(prev_state, state).items():
            for end in possible_moves:
                self._untried_actions.append((start,end))

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def is_terminal_node(self):
        return self.state.check_winning_state() != 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)



def mcts(prev_state, state, problem, remain_time):
    def _expand(current_node: MCTSNode):
        action = current_node._untried_actions.pop()
        next_state = problem.move(current_node.state, action)
        child_node = MCTSNode(
            current_node.state, next_state, problem, parent=current_node, parent_action=action)

        current_node.children.append(child_node)
        return child_node 

    def _tree_policy(current_node: MCTSNode):
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return _expand(current_node)
            else:
                current_node = current_node.best_child()
        return current_node

    def _rollout(node, max_depth = MAX_DEPTH):
        prev_rollout_state = node.prev_state
        current_rollout_state = node.state
        while current_rollout_state.check_winning_state() == 0: # game continue  
            # choose random move   
            dict_possible_moves = problem.get_possible_moves(prev_rollout_state,current_rollout_state)
            random_start = random.choice(list(dict_possible_moves.keys()))
            random_end = random.choice(dict_possible_moves[random_start])
            random_move = (random_start,random_end)
            # next state
            prev_rollout_state = current_rollout_state
            current_rollout_state = problem.move(current_rollout_state, random_move)

            max_depth -= 1
            if max_depth == 0: break

        # return current_rollout_state.check_winning_state()
        count_p1 = np.sum(current_rollout_state.board ==  1)
        count_p2 = np.sum(current_rollout_state.board == -1)
        diff = count_p1 - count_p2
        return (diff) / abs(diff) if diff != 0 else 0


    root = MCTSNode(prev_state, state, problem)
    while remain_time > 0:
        st_time = time.time() # time start

        v = _tree_policy(root)
        reward = _rollout(v)
        v.backpropagate(reward)

        ed_time = time.time() # time end
        remain_time -= ed_time-st_time

    return root.best_child().parent_action


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
            optimize action from all possible action.
            eg. ((1,1),(1,2)).  
    '''

    state = State(board, player)
    prev_state = State(prev_board, -player) if prev_board is not None else None
    problem = Problem()

    if player == 1:
        remain_time = remain_time_x/1000
    else:
        state.board *= -1
        state.player = 1
        if prev_state is not None:
            prev_state.board *= -1
            prev_state.player = -1

        remain_time = remain_time_y/1000
    remain_time = min(remain_time,TIME_THINKING)

    action = mcts(prev_state, state, problem, remain_time)

    return action

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
    player = -1
    a = move(prev_board, board, player, 5000, 5000)
    print(a)