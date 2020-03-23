import pygame
from mygame_gui_lib import Panel
from mygame_gui_lib import Button
import sys
class MainWindow:
    def __init__(self):
        # pygame.init()
        pygame.font.init()
        pygame.display.init()
        self.refresh_rate = 100
        self.main_clock = pygame.time.Clock()
        self.elements = []
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("practise algorithm by writing various game")
        self.set_default_layout()
        self.mouse_down_listener = []
        self.key_down_listener = []
        self.sys_exit_listener = []
        

    def set_default_layout(self):
        top_panel = Panel(height=30, width=800,background_color=(0,200,0))
        self.elements.append(top_panel)
        main_panel = Panel(y=30,height=570, width=600,background_color=(0,250,0))
        self.elements.append(main_panel)
        right_panel = Panel(y=30,x=600,height=570, width=200,background_color=(0,100,0))
        self.elements.append(right_panel)
    def add_top(self,elem):
        self.elements[0].add(elem)

    def add_main(self,elem):
        
        self.elements[1].add_to_center(elem)
    def refresh(self):
        for ele in self.elements:
            ele.reset()
        # self.elements[1].set_visible(False)

    
    # display window on the screen
    def show_window(self):
        # self.screen.fill((255,255,255), self.screen.get_rect())

        while True:
            # self.show_window()
            self.start_listen_event()
            for elem in self.elements:
                if elem.get_visible():
                    # elem.blit_elems()
                    surface, rect = elem.get_surface()
                    self.screen.blit(surface, rect)
            self.main_clock.tick(self.refresh_rate)
            pygame.display.flip()
    def get_main(self):
        return self.elements[1]
    def get_right(self):
        return self.elements[2]
    
    # stop game
    
        
    # response mouse down event
    def _process_mouse_down(self,pos):
        for elem in self.mouse_down_listener:
            if elem.can_response(pos) and  elem.response_mouse_down(pos, pygame.mouse.get_pressed()[0]):
                return

    # you must implement sys_exit() before add sys_exit listener 
    def _process_sys_exit(self):
        for elem in self.sys_exit_listener:
            elem.sys_exit()
        sys.exit(0)

    # response mouse down event
    def _process_key_down(self,key):
        for elem in self.key_down_listener:
            elem.response_key_down(key)
                


    def register_mouse_down(self,elem):
        self.mouse_down_listener.append(elem)
    
    def register_key_down(self,elem):
        self.key_down_listener.append(elem)

    def register_sys_exit(self,elem):
        self.sys_exit_listener.append(elem)

# begin to listen all event
    def start_listen_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._process_sys_exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._process_mouse_down(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                self._process_key_down(event.key)