import sys

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pygame_menu

from constants import *
from algorithms import alpha,beta,delta,epsilon,mcts_base,deep_ai
from gameUI import HVHGameUI,HVCGameUI,CVCGameUI

# Global Constant
ALGORITHM_CHOICES = [
    ('Alpha',alpha),
    ('Beta',beta),

    ('Delta',delta),
    ('Epsilon',epsilon),
    ('MCTS_BASE',mcts_base),
    ('DEEP_AI',deep_ai),
]

# Global Variable
CURRENT_STATE = 'MENU' # HvH, HvC, CvC, MENU
ALGORITHM_P1 = ALGORITHM_CHOICES[0][1]
ALGORITHM_P2 = ALGORITHM_CHOICES[0][1]

if __name__ == '__main__':

    # Init pygame
    pygame.init()

    # Game clock
    clock = pygame.time.Clock()

    # Create window
    surface = pygame.display.set_mode((W_WIDTH_SIZE,W_HEIGHT_SIZE))


    # -----------------------------------------------------------------------------
    # Computer vs Computer menu
    def cvc_play_game():
        global surface, menu, CURRENT_STATE, GAME, ALGORITHM_P1, ALGORITHM_P2
        # print(f'Computer {ALGORITHM_P1} vs Computer {ALGORITHM_P2}')
        menu.disable()
        GAME = CVCGameUI(surface, ALGORITHM_P1, ALGORITHM_P2)
        CURRENT_STATE ='CvC'

    def cvc_chose_algorithm_1(selected_value, algorithm, **kwargs):
        global ALGORITHM_P1
        ALGORITHM_P1 = algorithm

    def cvc_chose_algorithm_2(selected_value, algorithm, **kwargs):
        global ALGORITHM_P2
        ALGORITHM_P2 = algorithm

    cvc_menu = pygame_menu.Menu('Co Ganh', W_WIDTH_SIZE, W_HEIGHT_SIZE,
                                    onclose=None,
                                    theme=CUSTOME_THEME,
                                    mouse_motion_selection=True)

    cvc_menu.add.label('COMPUTER vs COMPUTER',font_size=40).set_margin(0, 30)

    cvc_menu.add.selector('Algorithm P1', 
                        items=ALGORITHM_CHOICES,
                        onchange=cvc_chose_algorithm_1,
                        font_size=28)

    cvc_menu.add.selector('Algorithm P2', 
                        items=ALGORITHM_CHOICES,
                        onchange=cvc_chose_algorithm_2,
                        font_size=28).set_margin(0, 20)

    cvc_menu.add.button('Fight', cvc_play_game)


    # -----------------------------------------------------------------------------
    # Human vs Computer menu
    def hvc_play_game():
        global surface, menu, CURRENT_STATE, GAME, ALGORITHM_P1
        # print(f'Human vs Computer {ALGORITHM_P1}')
        menu.disable()
        GAME = HVCGameUI(surface, ALGORITHM_P1)
        CURRENT_STATE ='HvC'

    def hvc_chose_algorithm(selected_value, algorithm, **kwargs):
        global ALGORITHM_P1
        ALGORITHM_P1 = algorithm

    hvc_menu = pygame_menu.Menu('Co Ganh', W_WIDTH_SIZE, W_HEIGHT_SIZE,
                                    onclose=None,
                                    theme=CUSTOME_THEME,
                                    mouse_motion_selection=True)

    hvc_menu.add.label('HUMAN vs COMPUTER',font_size=40).set_margin(0, 30)


    hvc_menu.add.selector('Algorithm', 
                        items=ALGORITHM_CHOICES,
                        onchange=hvc_chose_algorithm,
                        font_size=28).set_margin(0, 20)

    hvc_menu.add.button('Fight', hvc_play_game)


    # -----------------------------------------------------------------------------
    # Play menu
    def hvh_play_game():
        global surface, menu, CURRENT_STATE, GAME
        # print(f'Human vs Human')
        menu.disable()
        GAME = HVHGameUI(surface)
        CURRENT_STATE ='HvH'
        

    play_menu = pygame_menu.Menu('Co Ganh', W_WIDTH_SIZE, W_HEIGHT_SIZE,
                                onclose=None,
                                theme=CUSTOME_THEME,
                                mouse_motion_selection=True)

    play_menu.add.label('Option',font_size=40).set_margin(0, 30)
    play_menu.add.button('Hum vs Hum', hvh_play_game).set_margin(0, 5)
    play_menu.add.button('Hum vs Com', hvc_menu).set_margin(0, 5)
    play_menu.add.button('Com vs Com', cvc_menu).set_margin(0, 5)    


    # -----------------------------------------------------------------------------
    # Main menu
    menu = pygame_menu.Menu('Co Ganh', W_WIDTH_SIZE, W_HEIGHT_SIZE,
                            onclose=None,
                            theme=CUSTOME_THEME,
                            mouse_motion_selection=True,)

    menu.add.button('PLAY GAME', play_menu)
    menu.add.button('QUIT', pygame_menu.events.EXIT)


    # -----------------------------------------------------------------------------
    # Main loop
    while True:
        # tick clock
        deltatime = clock.tick(FPS)

        # all game events
        events = pygame.event.get()

        if CURRENT_STATE in ['HvH','HvC','CvC']:
            if CURRENT_STATE == 'HvH':
                GAME.process(events)
            else:
                GAME.process(events,deltatime)
                
            if GAME.should_quit():
                CURRENT_STATE = 'MENU'
                menu.enable()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        try:
            menu.mainloop(surface)
        except:
            pass

        pygame.display.update()
