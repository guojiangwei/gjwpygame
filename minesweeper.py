
import random
import time
import pygame
from mygame_gui_lib import Button
from mygame_gui_lib import Panel
from mygame_gui_lib import OptionButton
import os
from mygame_framework import *
from  settings import Settings
class MainSweeper(AbstractGame):
    def __init__(self, main_game):
        super().__init__(main_game)
        # self.level = 1
        self.game_panel = MineSweeper(self)
        self.main_window.add_main(self.game_panel)
        self.sb = ScoreBoard(self)
        self.main_window.register_mouse_down(self.game_panel)
        self.main_window.register_mouse_down(self.sb)
        


        self.game_result = GameResult(self)
        self.main_window.add_main(self.game_result)
        self.main_window.register_mouse_down(self.game_result)

        self.set_active(False)

    def reset_game(self):
        print("reset sweeper game!")
        # self.game_panel.set_level(1)
        super().reset_game()
        self.main_window.refresh()
        
    def start_game(self):
        super().start_game()
        # self.sb.set_curr_label('0')
        # self.sb.set_level(str(self.level))
        self.level = self.sb.get_level()
        self.sb.set_mine_num_label(str(self.game_panel._mine_nums))
    
    def add_time(self):
        # super().add_time()
        self.current_score += 1
        self.sb.set_score(str(self.current_score))
    def set_level(self,level):
        self.game_panel.set_level(level)
        self.reset_game()

# 显示每个单元格，每个单元可以存放地雷，也可以点击
class SweeperGrid(Button):
    def __init__(self,row = 0, col = 0, x = 0,y = 0, height = 10, width = 10, image = '', text = '', text_color = (0, 0, 0), background_color = (255, 255, 255)):
        super(SweeperGrid,self).__init__(x = x, y = y, height = height, width = width, image = image, text = text, text_color = text_color, background_color = background_color)
        self._content = {'mine':"resources/mine.png",'redflag':"resources/redflag.png",'bomb':'resources/mine-bomb.png'}
        self.set_border_color((100,200,100))
    def repose_mouse_down(self,pos , mouse_index = 0):
        # print(mouse_index)
        if self.contain_point(pos):
            print(mouse_index)
            if mouse_index == 0:
                self.change_grid_content('mine')
            elif mouse_index == 1:
                self.change_grid_content('redflag')
                # self.set_image(os.path.abspath("mygame/resources/redflag.png"))
            return True
        return False
    def change_grid_content(self, content):
        
        self.set_image(Settings.resource_path+self._content[content])

        

class MineSweeper(AbstractGamePanel):
    def __init__(self, main_sweeper, level=1):
        parent_window = main_sweeper.get_game_panel()
        self._rows = 9
        self._cols = 9
        self._max_rows = 16
        self._max_cols = 30
        self._mine_nums = 10
        self.grid_color = (0,0,255)
        self.mine_grid = [  [ 'E' for _ in range(self._max_cols)] for _ in range(self._max_rows) ]
        self.graph_grid = [  [] for _ in range(self._max_rows) ]
        self.init_level(level)
        
        super(MineSweeper,self).__init__(main_game=main_sweeper, height=parent_window.get_height()-10,width=parent_window.get_width()-10)
        # status: 0 initial, 1 failed, 2 success, 3,playing
        # 初始化表格图像 和 表格控件，表格控件就是按钮
    def init_graph_grid(self):
        for i in range(self._max_rows):
            for j in range(self._max_cols):
                button = SweeperGrid( background_color=self.grid_color)
                button.set_visible(False)
                self.graph_grid[i].append(button)
                self.add(button)
                
        # 重置游戏每个游戏都需要实现自己的reset方法，并且调用父类的reset方法
    def reset_game(self):
        if len(self.graph_grid[0]) == 0:
            self.init_graph_grid()
        super().reset_game()
        self.init_level(self._level)

        self.create_graph_grid()
        self.create_grid()
    # 根据级别显示对应数量的表格  ， 并将超过本级别数量的表格隐藏，地雷二维数组值全部为0，
    def create_graph_grid(self):
        # if self.active:
        dx = (self._width/self._cols)
        dy = (self._height/self._rows)
        
        for i in range(self._max_rows):
            for j in range(self._max_cols):
                if i < self._rows and j < self._cols:
                    self.graph_grid[i][j].set_visible(True)
                    self.graph_grid[i][j].set_position( dx * j, dy * i)
                    self.graph_grid[i][j].set_width(dx+1)
                    self.graph_grid[i][j].set_height(dy+1)
                    self.graph_grid[i][j].set_image("")
                    self.graph_grid[i][j].set_bgcolor(self.grid_color)
                else:
                    self.graph_grid[i][j].set_visible(False)
                
                
    # 设置级别，每个级别拥有不同数量点表格和不同数量的地雷
    def init_level(self, level=1):
        self._level = level
        if level == 1:
            self._rows = 9
            self._cols = 9
            self._mine_nums = 10
            # self.create_grid(9,9,10)
        elif level == 2:
            self._rows = 16
            self._cols = 16
            self._mine_nums = 40
            # self.create_grid(16,16,40)
        elif level == 3:
            self._rows = 16
            self._cols = 30
            self._mine_nums = 99
    def set_level(self, level):
        self.init_level(level)
        # self.reset_game()
            # self.create_grid(16,30,99)
# 随机挑选有地雷的表格，地雷由字母 M 表示
    def create_grid(self):
        random.seed(time.time())
        nums = 0
        self.mine_grid = [  [ 'E' for _ in range(self._max_cols)] for _ in range(self._max_rows) ]
        while True:
            m = random.randint(0,self._rows - 1)
            n = random.randint(0,self._cols - 1)
            if self.mine_grid[m][n] != 'M':
                self.mine_grid[m][n] = 'M'
                nums += 1
                if nums == self._mine_nums :
                    break
                # judge whether there is a sweeper in specified position
    def _exist_sweeper(self, row, col):
        return self.mine_grid[row][col] == 'M' 
    def gameover(self, status):
        
        self.running = False
        
        for i in range(self._rows):
            for j in range(self._cols):
                self.graph_grid[i][j].active = False
                if self.mine_grid[i][j] in ['M', 'm']:
                    self.graph_grid[i][j].change_grid_content('mine')
        self.main_game.stop_game(status)
# get the amount of mine which is not mined
    def get_true_mine_nums(self):
        count = 0
        for rows in self.mine_grid:
            for mine in rows:
                if mine == 'M':
                    count += 1
        return  count 

    def response_mouse_down(self,pos , mouse_index = 0):
        pos = self._convert_to_relatepos(pos)
        if self.running:
            for i in range(self._rows):
                for j in range(self._cols):
                    if self.graph_grid[i][j].active and self.graph_grid[i][j].contain_point(pos) :     
                        if mouse_index == 1: #left button
                            if self._exist_sweeper(i,j):
                                self.graph_grid[i][j].change_grid_content('bomb')
                                self.gameover(1) # failed
                            else:
                                self.span_mine(i,j)
                                
                                self.update_graph_grid( )
                        elif mouse_index == 0: #right button
                            self.mine_grid[i][j] = 'm'
                            self._mine_nums -= 1
                            
                            if self._mine_nums < 2 and self.get_true_mine_nums() == self._mine_nums and self.count_unmined_grid() == 2:
                                self._mine_nums = 0
                            if self._mine_nums == 0:
                                self.gameover(0) # success
                                # self.main_game.
                                return
                            self.main_game.sb.set_mine_num_label(str(self._mine_nums))
                            self.graph_grid[i][j].change_grid_content('redflag')

                        
                        return True
        
        return False
    def count_unmined_grid(self):
        count = 0
        for i in range(self._rows):
            for j in range(self._cols):
                if self.mine_grid[i][j] in ['E', 'M']:
                    print("i,j:", i, j)
                    count += 1
        print("count:",count)
        return  count
        # sweep mine algorithm
    def update_graph_grid(self):
        for i in range(self._rows):
            for j in range(self._cols):
                if self.mine_grid[i][j] == 'B':
                    self.graph_grid[i][j].set_bgcolor((200,200,200))
                elif self.mine_grid[i][j] != 'B' and self.mine_grid[i][j] != 'm' and self.mine_grid[i][j] != 'E' and self.mine_grid[i][j] != 'M':
                    # print("update grid text:", self.mine_grid[i][j])
                    self.graph_grid[i][j].set_text(self.mine_grid[i][j])

    def span_mine(self,row, col):
        directions = [[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1]]
        def get_mine_num(i, j):
            count = 0
            for direction in directions:
                new_i = i + direction[0]
                new_j = j + direction[1]
                if 0 <= new_i and new_i < self._rows and 0 <= new_j < self._cols and self.mine_grid[new_i][new_j] in ['M', 'm']:
                    count +=1
            return count
        def dfs(i= row,j=col):
            mine_nums = get_mine_num(i, j)
            if 0 < mine_nums:
                print("remain mine amount around the grid:" ,mine_nums)
                self.mine_grid[i][j] = str(mine_nums)
            else:
                for direction in directions:
                    new_i = i + direction[0]
                    new_j = j + direction[1]
                    if 0 <= new_i and new_i < self._rows and 0 <= new_j < self._cols and self.mine_grid[new_i][new_j] == 'E':
                        self.mine_grid[new_i][new_j] = 'B'
                        dfs(new_i, new_j)
        dfs(row,col)
class ScoreBoard(AbstractScoreBoard):
    def __init__(self,minesweeper):
        super().__init__(minesweeper)
        ym = self.center_y - 30
        xm = 2 * self.center_x - 3
        self.level_label = OptionButton([1, 2, 3],x=2, y= ym, width= xm, height= self.height+30,background_color=self.color)
        self.add(self.level_label)
        self.set_item_label(1,'mine')


    def set_active(self, value):
        super().set_active(value)
        self.level_label.set_visible(value)

    # def set_level(self, level):
    #     self.level_label.set_text(level)
    def get_level(self):
        return self.level_label.current_value

    def set_mine_num_label(self, num):
        self.set_item_value(1,str(num))

    def  response_mouse_down(self,pos , mouse_index = 0):
        if not self.main_game.running:
            result = self.level_label.response_mouse_down(pos, mouse_index)
            if result :
                self.main_game.set_level(self.get_level())
            return result
    
    def can_response(self, pos):
        return self.level_label.can_response(pos)
        
