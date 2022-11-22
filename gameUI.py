import pygame

from algorithms import State,Problem
from constants import *

# Base GameUI class
class BaseGameUI:
    def __init__(self, surface, w_height_size, w_width_size, max_move, max_total_time):
        self.surface = surface
        self.W_HEIGHT_SIZE = w_height_size
        self.W_WIDTH_SIZE  = w_width_size
        self.CENTER_X = W_WIDTH_SIZE / 2
        self.CENTER_Y = W_HEIGHT_SIZE / 2

        self.remain_move = max_move
        self.max_total_time = max_total_time
        self.problem = Problem()

        self.over = False
        self.ESC = False
    
    def process_input(self, event):
        pass

    def draw(self):
        pass

    def process_end(self):
        pass

    def process(self, event):
        self.process_input(events)
        self.draw()
        self.process_end()

    def should_quit(self):
        return self.ESC


# Game UI for Hum vs Hum
class HVHGameUI(BaseGameUI):
        def __init__(self, surface, w_height_size=W_HEIGHT_SIZE, w_width_size=W_WIDTH_SIZE,\
                     max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
            super(HVHGameUI,self).__init__(surface, w_height_size, w_width_size, max_move, max_total_time)

        def process_input(self, event):
            pass
    
        def process_end(self):
            pass
        

# Game UI for Hum vs Com
class HVCGameUI(BaseGameUI):
        def __init__(self, surface, algorithm, w_height_size=W_HEIGHT_SIZE, w_width_size=W_WIDTH_SIZE,\
                     max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
            super(HVCGameUI,self).__init__(surface, w_height_size, w_width_size, max_move, max_total_time)
            self.algorithm = algorithm

        def process_input(self, event):
            pass
    
        def process_end(self):
            pass
        

# Game UI for Com vs Com
class CVCGameUI(BaseGameUI):
        def __init__(self, surface, algorithm1, algorithm2, w_height_size=W_HEIGHT_SIZE,\
                     w_width_size=W_WIDTH_SIZE, max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
            super(CVCGameUI,self).__init__(self, surface, w_height_size, w_width_size, max_move, max_total_time)
            
            self.algorithm1 = algorithm1
            self.algorithm2 = algorithm2
        
        def process_input(self, event):
            pass
    
        def process_end(self):
            pass
        


if __name__ == '__main__':
    # Test Space