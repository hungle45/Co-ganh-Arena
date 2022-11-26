import copy
import sys

import pygame

from algorithms import State,Problem
from constants import *

# Base GameUI class
class BaseGameUI:
    def __init__(self, surface, w_height_size, w_width_size, max_move, max_total_time):
        self.surface = surface

        self.W_HEIGHT_SIZE = w_height_size
        self.W_WIDTH_SIZE  = w_width_size
        self.CENTER_X = self.W_WIDTH_SIZE / 2
        self.CENTER_Y = self.W_HEIGHT_SIZE / 2

        self.problem = Problem()
        self.state = copy.deepcopy(self.problem.init_state)

        self.SQUARE_SIZE = 90
        self.START_X = self.CENTER_X - self.SQUARE_SIZE*2
        self.START_Y = self.CENTER_Y - self.SQUARE_SIZE*2

        self.remain_move = max_move
        self.max_total_time = max_total_time

        self.player_to_move = 1 # 1: blue; -1: red
        self.move_log = []

        self.over = False
        self.ESC = False

    def _get_coord_by_index(self,x,y):
        x = self.START_X + self.SQUARE_SIZE*x
        y = self.START_Y + self.SQUARE_SIZE*y
        return x,y


    def _process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ESC = True


    def _draw_grid(self):
        for i in range(5):
            pygame.draw.line(self.surface,'black',
                self._get_coord_by_index(i,0),self._get_coord_by_index(i,4),2)

            pygame.draw.line(self.surface,'black',
                self._get_coord_by_index(0,i),self._get_coord_by_index(4,i),2)

    def _draw_diagonal(self):
        # big cross
        pygame.draw.line(self.surface,'black',
            self._get_coord_by_index(0,0),self._get_coord_by_index(4,4),2)
        pygame.draw.line(self.surface,'black',
            self._get_coord_by_index(4,0),self._get_coord_by_index(0,4),2)

        # small rotated square
        encoded_coords = [2,0,2,4,2,0]
        for i in range(4):
            pygame.draw.line(self.surface,'black',
                self._get_coord_by_index(encoded_coords[i],encoded_coords[i+1]),
                self._get_coord_by_index(encoded_coords[i+1],encoded_coords[i+2]),2)

    def _draw_intersection_point(self,x,y):
        pygame.draw.circle(self.surface,'white',self._get_coord_by_index(x,y),4)
        pygame.draw.circle(self.surface,'black',self._get_coord_by_index(x,y),4,2)

    def _draw_piece(self,color,x,y):
        pygame.draw.circle(self.surface,color,self._get_coord_by_index(x,y),12)

    def _draw_board(self):
        # board background
        pygame.draw.rect(self.surface,'white',
            (self.CENTER_X-500/2,self.CENTER_Y-500/2,500,500))

        # raw board
        self._draw_grid()
        self._draw_diagonal()
        
        # draw pieces
        for x in range(5):
            for y in range(5):
                if self.state.board[x][y] == 1:
                    self._draw_piece('blue', x, y)
                elif self.state.board[x][y] == -1:                    
                    self._draw_piece('red', x, y)
                else:
                    self._draw_intersection_point(x,y)

    def _draw(self):
        self.surface.fill(BG_COLOR)
        self._draw_board()


    def _process_end(self):
        pass

    def process(self, events):
        self._process_input(events)
        self._draw()
        self._process_end()

    def should_quit(self):
        return self.ESC


# Game UI for Hum vs Hum
class HVHGameUI(BaseGameUI):
        def __init__(self, surface, w_height_size=W_HEIGHT_SIZE, w_width_size=W_WIDTH_SIZE,\
                     max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
            super(HVHGameUI,self).__init__(surface, w_height_size, w_width_size, max_move, max_total_time)

        def _process_input(self, events):
            super(HVHGameUI,self)._process_input(events)
    
        def _process_end(self):
            super(HVHGameUI,self)._process_end()
        

# Game UI for Hum vs Com
class HVCGameUI(BaseGameUI):
        def __init__(self, surface, algorithm, w_height_size=W_HEIGHT_SIZE, w_width_size=W_WIDTH_SIZE,\
                     max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
            super(HVCGameUI,self).__init__(surface, w_height_size, w_width_size, max_move, max_total_time)
            self.algorithm = algorithm

        def _process_input(self, events):
            super(HVCGameUI,self)._process_input(events)
    
        def _process_end(self):            
            super(HVHGameUI,self)._process_end()
        

# Game UI for Com vs Com
class CVCGameUI(BaseGameUI):
        def __init__(self, surface, algorithm1, algorithm2, w_height_size=W_HEIGHT_SIZE,\
                     w_width_size=W_WIDTH_SIZE, max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
            super(CVCGameUI,self).__init__(self, surface, w_height_size, w_width_size, max_move, max_total_time)
            
            self.algorithm1 = algorithm1
            self.algorithm2 = algorithm2
        
        def _process_input(self, events):
            pass
    
        def _process_end(self):
            pass
        


if __name__ == '__main__':
    # Test Space
    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((W_WIDTH_SIZE,W_HEIGHT_SIZE))

    GAME = HVHGameUI(surface)

    while True:
        # tick clock
        deltatime = clock.tick(FPS)

        # all game events
        events = pygame.event.get()

        GAME.process(events)

        for event in events:
            if event.type == pygame.QUIT or GAME.should_quit():
                pygame.quit()
                sys.exit()

        try:
            menu.mainloop(surface)
        except:
            pass
        
        pygame.display.update()