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
        self.PIECE_RADIUS = 20

        self.remain_move_p1 = self.remain_move_p2 = max_move
        self.max_total_time = max_total_time

        self.move_log = []
        self.selected_piece = None

        self.over = False
        self.ESC = False

    def _get_coord_by_index(self,x,y):
        x = self.START_X + self.SQUARE_SIZE*x
        y = self.START_Y + self.SQUARE_SIZE*y
        return x,y

    def _move(self,action):
        self.move_log.append(copy.deepcopy(self.state)) # save move for undo feature

        can_do, _ = self.problem.move_if_possible(self.state,action,inplace=True)
        if can_do:
            if self.state.player == -1:
                self.remain_move_p1 -= 1
            else:
                self.remain_move_p2 -= 1

        return can_do

        # simulate move action
        self.state.board[action[1]] = self.state.board[action[0]]
        self.state.board[action[0]] = 0
        self.state.player *= -1
        return True


    def _process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ESC = True


    def _draw_grid(self):
        for i in range(5):
            pygame.draw.line(self.surface,BLACK,
                self._get_coord_by_index(i,0),self._get_coord_by_index(i,4),2)

            pygame.draw.line(self.surface,BLACK,
                self._get_coord_by_index(0,i),self._get_coord_by_index(4,i),2)

    def _draw_diagonal(self):
        # big cross
        pygame.draw.line(self.surface,BLACK,
            self._get_coord_by_index(0,0),self._get_coord_by_index(4,4),2)
        pygame.draw.line(self.surface,BLACK,
            self._get_coord_by_index(4,0),self._get_coord_by_index(0,4),2)

        # small rotated square
        encoded_coords = [2,0,2,4,2,0]
        for i in range(4):
            pygame.draw.line(self.surface,BLACK,
                self._get_coord_by_index(encoded_coords[i],encoded_coords[i+1]),
                self._get_coord_by_index(encoded_coords[i+1],encoded_coords[i+2]),2)

    def _draw_intersection_point(self,r,c):
        pygame.draw.circle(self.surface,WHITE,self._get_coord_by_index(r,c),4)
        pygame.draw.circle(self.surface,BLACK,self._get_coord_by_index(r,c),4,2)

    def _draw_piece(self,color,x,y,radius=None):
        if radius is None:
            radius = self.PIECE_RADIUS
        pygame.draw.circle(self.surface,color,self._get_coord_by_index(x,y),radius)

    def _draw_board(self):
        # board background
        pygame.draw.rect(self.surface,WHITE,
            (self.CENTER_X-500/2,self.CENTER_Y-500/2,500,500))

        # raw board
        self._draw_grid()
        self._draw_diagonal()

    def _draw_player_info(self,title,text_color,pos):
        # render background
        pygame.draw.rect(self.surface,WHITE,
            (pos[0]-80,pos[1]-80,160,150))
        pygame.draw.rect(self.surface,text_color,
            (pos[0]-80,pos[1]-80,160,150),1,8)

        # render title
        text = pygame.font.Font(None, 30).render(title, True, text_color)
        text_rect = text.get_rect(center=(pos[0],pos[1]-50))
        self.surface.blit(text, text_rect)

    def _draw(self):
        self.surface.fill(BG_COLOR)
        self._draw_board()

        # draw pieces
        for x in range(5):
            for y in range(5):
                if self.state.board[x][y] == 1:
                    self._draw_piece(P1_COLOR, x, y)
                elif self.state.board[x][y] == -1:                    
                    self._draw_piece(P2_COLOR, x, y)
                else:
                    self._draw_intersection_point(x,y)
                    
        # Player infor
        text_color_p1,text_color_p2 = (BLACK,GRAY) \
            if self.state.player == 1 else (GRAY,BLACK)
        self._draw_player_1_info(text_color_p1,
            (self.W_WIDTH_SIZE/2-345,self.W_HEIGHT_SIZE/2))
        self._draw_player_2_info(text_color_p2,
            (self.W_WIDTH_SIZE/2+345,self.W_HEIGHT_SIZE/2))

        # Instruction
        text = pygame.font.Font(None, 24).render('Press R to undo', True, (108, 117, 125))
        text_rect = text.get_rect(center=(self.W_WIDTH_SIZE/2, self.W_HEIGHT_SIZE - 35))
        self.surface.blit(text, text_rect)


    def _process_end(self):
        pass


    def process(self, events):
        self._process_input(events)
        self._draw()
        self._process_end()

    def should_quit(self):
        return self.ESC




class HumanGameUIMixin():
    def _get_index_by_mouse_pos(self,pos):
        pos_x,pos_y = pos[0]-self.START_X, pos[1]-self.START_Y

        nearest_row = round(pos_x/self.SQUARE_SIZE)
        nearest_col = round(pos_y/self.SQUARE_SIZE)

        r,c = None,None
        if 0<=nearest_row<5 and abs(pos_x-self.SQUARE_SIZE*nearest_row)<=self.PIECE_RADIUS:
            r = nearest_row
        if 0<=nearest_col<5 and abs(pos_y-self.SQUARE_SIZE*nearest_col)<=self.PIECE_RADIUS:
            c = nearest_col

        return r, c

    def _handle_select_piece(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            r,c = self._get_index_by_mouse_pos(pos)

            if r is not None and c is not None:
                if self.selected_piece is None:
                    if self.state.player == self.state.board[r][c]:
                        self.selected_piece = (r,c)
                else:
                    if self.selected_piece == (r,c):
                        self.selected_piece = None
                    else:
                        if self._move((self.selected_piece,(r,c))):
                            self.selected_piece = None
    
    def _handle_undo(self,event):
        if event.key == pygame.K_u and len(self.move_log) != 0:
            self.state = self.move_log.pop()
            if self.state.player == 1:
                self.remain_move_p1 += 1
            else:
                self.remain_move_p2 += 1
            

    def _draw_seleted_piece(self):
        if self.selected_piece is not None:
            if self.state.board[self.selected_piece] == 1:
                self._draw_piece((152, 193, 254),self.selected_piece[0],
                    self.selected_piece[1],self.PIECE_RADIUS+4)
                self._draw_piece(FOCUS_P1_COLOR,self.selected_piece[0],self.selected_piece[1])
            elif self.state.board[self.selected_piece] == -1:  
                self._draw_piece((240, 169, 176),self.selected_piece[0],
                    self.selected_piece[1],self.PIECE_RADIUS+4)                  
                self._draw_piece(FOCUS_P2_COLOR,self.selected_piece[0],self.selected_piece[1])

    def _draw_possible_moves(self):
        if self.selected_piece is not None:
            p_moves = self.problem.get_possible_moves(self.state).get(self.selected_piece,[])
            for p_move in p_moves:
                self._draw_piece((180, 180, 180),p_move[0],p_move[1],self.PIECE_RADIUS*0.6)



# Game UI for Hum vs Hum
class HVHGameUI(BaseGameUI,HumanGameUIMixin):
    def __init__(self, surface, w_height_size=W_HEIGHT_SIZE, w_width_size=W_WIDTH_SIZE,\
                    max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
        super(HVHGameUI,self).__init__(surface, w_height_size, w_width_size, max_move, max_total_time)

    def _process_input(self, events):
        super(HVHGameUI,self)._process_input(events)

        for event in events:
            if not self.over:
                self._handle_select_piece(event)
                if event.type == pygame.KEYDOWN:
                    self._handle_undo(event)


    def _draw_player_1_info(self, text_color, pos):
        super(HVHGameUI, self)._draw_player_info('Player 1',text_color, pos)

        text = pygame.font.Font(None, 24).render(
            f'Remain move: {self.remain_move_p1}', True, text_color)
        text_rect = text.get_rect(center=(pos[0],pos[1]-20))
        self.surface.blit(text, text_rect)

    def _draw_player_2_info(self, text_color, pos):        
        super(HVHGameUI, self)._draw_player_info('Player 2',text_color, pos)

        text = pygame.font.Font(None, 24).render(
            f'Remain move: {self.remain_move_p2}', True, text_color)
        text_rect = text.get_rect(center=(pos[0],pos[1]-20))
        self.surface.blit(text, text_rect)

    def _draw(self):
        super(HVHGameUI,self)._draw()
        self._draw_seleted_piece()
        self._draw_possible_moves()
    



# Game UI for Hum vs Com
class HVCGameUI(BaseGameUI):
    def __init__(self, surface, algorithm, w_height_size=W_HEIGHT_SIZE, w_width_size=W_WIDTH_SIZE,\
                    max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
        super(HVCGameUI,self).__init__(surface, w_height_size, w_width_size, max_move, max_total_time)
        self.algorithm = algorithm




# Game UI for Com vs Com
class CVCGameUI(BaseGameUI):
    def __init__(self, surface, algorithm1, algorithm2, w_height_size=W_HEIGHT_SIZE,\
                    w_width_size=W_WIDTH_SIZE, max_move=MAX_MOVE, max_total_time=MAX_TOTAL_TIME):
        super(CVCGameUI,self).__init__(self, surface, w_height_size, w_width_size, max_move, max_total_time)
        
        self.algorithm1 = algorithm1
        self.algorithm2 = algorithm2
        



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