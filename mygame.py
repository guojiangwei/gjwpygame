import pygame
from mygame_gui_lib import Panel
from mygame_gui_lib import Button
from main_window import MainWindow
import sys
# from minesweeper import MineSweeper
from minesweeper import MainSweeper
from russia_box import MainRussiaBox
import os
from settings import Settings
import types
class PlayGameButton(Button):
    def __init__(self,mainwindow,text='Play Game!',width=150):
        super(PlayGameButton, self).__init__(text=text,width=width)
        self.main_window = mainwindow
    def response_mouse_down(self, pos, mouse_index=0):
        if self._visible:
            self.set_visible(False)
            self.main_window.start()
            return True
        return False

class ChoiceGameButton(Button):
    def __init__(self,mainwindow,text,value,x=0, width=150):
        super(ChoiceGameButton, self).__init__(text=text,width=width,x=x)
        self.main_window = mainwindow
        self.value = value
    def response_mouse_down(self, pos, mouse_index=0):
        self.main_window.set_game(self.value)
        return True

class MainGame:
    def __init__(self):
        self.current_game = None
        self.main_window = MainWindow()

        main_sweeper = MainSweeper(self)
        main_russia = MainRussiaBox(self)
        self.games = [['sweeper', main_sweeper], ['RussiaBox', main_russia]]
        self.set_game(1)

        color = (200, 200, 200)
        self.exit_button = Button(text="exit", background_color=color)
        self.sweep_button = ChoiceGameButton(mainwindow=self,width=80, text=self.games[0][0],value=0)
        self.russiabox_button = ChoiceGameButton(mainwindow=self,width=100, x=82, text=self.games[1][0], value=1)
        self.main_window.register_mouse_down(self.russiabox_button)
        self.main_window.register_mouse_down(self.sweep_button)

        self.main_window.add_top(self.exit_button)
        self.exit_button.set_right()
        self.main_window.add_top(self.sweep_button)
        self.main_window.add_top(self.russiabox_button)

        
        
        # self.play_button = PlayGameButton(self)
        # self.main_window.add_main(self.play_button)
        # self.main_window.register_mouse_down(self.play_button)
        # self.game_result = GameResult(self)
        # self.main_window.add_main(self.game_result)
        # self.main_window.register_mouse_down(self.game_result)

        self.main_window.register_sys_exit(self)

        self.main_window.show_window()


         # 0 represent sweeper
    
    def refresh_rate(self):
        self.main_window.refresh_rate = self.current_game.get_refresh_rate()
    def start(self):
        self.current_game.start_game()

    def set_game(self, game):
        if self.current_game is not None:
            # self.stop_game()
            self.main_window.refresh()
            self.current_game.reset_game()
            self.current_game.set_active(False)
        
        self.current_game = self.games[game][1]
        print("set_game:"+str(game))
        self.current_game.set_active(True)
        # self.game_result.reset()


    
    def get_game_panel(self):
        # print("test:", self.main_window.get_main())
        return self.main_window.get_main()
    # def stop_game(self):
    #     # self.play_button.set_visible(True)
    #     self.game_result.set_status(0)
    #     # self.play_button.active = True
    #     # self.play_button.set_text("Play Game!")

    # def done_success(self):
    #     self.game_result.set_status(0)

    # def done_failed(self):
    #     self.game_result.set_status(1)
    #     # self.play_button.set_text("Play Game!")


# success   
#failed
    def sys_exit(self):
        print("sys exit")
        # self.stop_game()
        self.current_game.stop_game()
        
    # def start_game(self):

    #     while True:
    #         self.main_window.show_window()
    #         self.main_window.start_listen_event()



if __name__ == "__main__":
    print(os.getcwd())
    print(sys.argv)
    command_str = sys.argv[0]
    
    Settings.resource_path = sys.argv[0][:-9] if command_str[0] == '/' else os.getcwd() + '/' + sys.argv[0][:-9]

    print('settings:'+Settings.resource_path)
    main_game = MainGame()
    # main_game.start_game()

    
    

    

        
        


