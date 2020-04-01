from mygame_framework import *
import pygame
import random
import threading

class MainSudoku(AbstractGame):
    def __init__(self, main_game):
        super().__init__(main_game)
        
        self.game_panel = SudokuPanel(self)
        self.main_window.add_main(self.game_panel)
        main_game.main_window.register_key_down(self.game_panel)
        self.main_window.register_mouse_down(self.game_panel)
        self.game_name = 'sudoku'

        self.sb = ScoreBoard(self)
        self.main_window.register_mouse_down(self.sb)

        self.game_result = GameResult(self)
        self.main_window.add_main(self.game_result)
        self.main_window.register_mouse_down(self.game_result)

        self.set_active(False)
    def start_game(self):
        super().start_game()

        # 重载游戏计时方法，用时间来计算分数
    def add_time(self):
        self.time += 1
        self.sb.set_score(str(self.time))
    def solve_sudoku(self):
        self.game_panel.solve_sudoku()
    
    # def stop_game(self):
    #     super().stop_game()
    # def reset_game(self):
    #     super().reset_game()

class SudokuPanel(AbstractGamePanel):
    def __init__(self, main_sudoku, level=1):
        self.sudoku_data = [['.' for _ in range(9)] for _ in range(9)]
        self.result_sudoku_data = [] 
        self.display_rate = 100
        self.result_lock = threading.Lock()
        self.result_display_done = False
        self.sudoku_grid = [[] for _ in range(9)] 
        self.digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        # self.level = level
        self.set_level(level)
        self.digit_count = 20
        self.grid_size = 50
        self.grid_color = (200,10,0)
        self.active_grid_color = (150,10,0)
        self.active_grid_posi = (0, 0)
        super(SudokuPanel,self).__init__( main_game=main_sudoku,height=self.grid_size * 9 + 4,width=self.grid_size * 9 + 4)
        self.create_soduku_grid()

        
    def reset_game(self):
        print('reset sudoku!', self.running)
        super().reset_game()
        self.init_soduku_data()
        self.init_soduku_grid()

        # self.set_level(self.level)
    def set_level(self, level):
        self.level = level
        if level == 1:
            self.digit_count = 25
        elif level == 2:
            self.digit_count = 23
        elif level == 3:
            self.digit_count == 21
        elif level == 4:
            self.digit_count == 17
    def init_soduku_data(self):
        self.sudoku_data = [['.' for _ in range(9)] for _ in range(9)]
        count = self.digit_count
        print('count:{}'.format(count))
        while True:
            digit = random.choice(self.digits) 
            row = random.randint(1, 8)
            col = random.randint(1, 8)
            if self.sudoku_data[row][col] == '.' and self.can_place(col=col, row=row,ch=digit):
                self.sudoku_data[row][col] = digit
                count -= 1
            if count == 0:
                break
        # print(self.sudoku_data)
    def create_soduku_grid(self):
        for i in range(9):
            y = i*self.grid_size
            
            if i % 3 == 0:
                    y += 2
            
            for j in range(9):
                x = j*self.grid_size
                if j % 3 == 0:
                    x += 2
                grid = Button(x=x, y=y,width=self.grid_size,height=self.grid_size, background_color=self.grid_color)
                self.add(grid)
                self.sudoku_grid[i].append(grid)
            self.sudoku_grid[self.active_grid_posi[0]][self.active_grid_posi[1]].set_bgcolor(self.active_grid_color)
    def init_soduku_grid(self):
        print(self.sudoku_data)
        for i in range(9):
            for j in range(9):
                # self.sudoku_grid[i][j].set_text('11')
                if self.sudoku_data[i][j] == '.':
                    self.sudoku_grid[i][j].set_text('')
                else:
                    # print('inner: ',self.sudoku_data[i][j])
                    self.sudoku_grid[i][j].set_text(self.sudoku_data[i][j])
                    

    # 检查给定定点位置是否可以存放给定点字符
    def can_place(self, col, row, ch):
        # 检查行是否满足要求
        def check_row(i, c):
            for j in range(9):
                if self.sudoku_data[i][j] == c:
                    return False
            return True
        # 检查列是否满足要求
        def check_col(j, c):
            for i in range(9):
                if self.sudoku_data[i][j] == c:
                    return False
            return True
        # 检查小方格是否满足要求
        def check_box(boxrow, boxcol, c):
            for i in range(boxrow, boxrow+3):
                for j in range(boxcol, boxcol+3):
                    # print('i,j=',i,j,c)
                    # print(self.sudoku_data[i][j])
                    if self.sudoku_data[i][j] == c:
                        return False
            return True
        
        boxrow = row - row%3
        boxcol = col - col%3

        if check_row(row, ch) and check_col(col, ch) and check_box(boxrow, boxcol, ch):
            return True
        return False
    # 破解数度方法， 包括两部分
    # 1，生成破解的矩阵
    # 2，每一步填充一个方格，
    # 3，每次填充方法间隔一定的时间，动态显示在屏幕上
    def find_empty_grid(self):
        for row in range(9):
            for col in range(9):
                if self.sudoku_data[row][col] == '.':
                    return row, col
        return -1, -1
    def solve(self):
        # print('solve1')
        row, col = self.find_empty_grid()
        if row == -1 or col == -1:
            return True
        for d in self.digits:
            if self.can_place(row=row, col=col, ch=d):
                self.sudoku_data[row][col] = d
                self.result_sudoku_data.append((row, col, d))
                # self.result_sudoku_data[row][col] = d
                if self.solve():
                    return True
                self.sudoku_data[row][col] = '.'
                self.result_sudoku_data.pop()
                
        return False
                        
                
    def get_surface(self):
        self.result_lock.acquire()
        if len(self.result_sudoku_data) > 0:
            # print('rate:',self.display_rate)
            
            if self.display_rate == 0:
                self.sudoku_grid[self.active_grid_posi[0]][self.active_grid_posi[1]].set_is_fade_in(False)
                grid = self.result_sudoku_data.pop()
                if len(self.result_sudoku_data) == 0:
                    self.result_display_done = True
                self.active_grid_posi = tuple((grid[0], grid[1]))
                self.sudoku_grid[grid[0]][grid[1]].set_text(grid[2])
                self.sudoku_grid[grid[0]][grid[1]].set_is_fade_in(True)
                self.display_rate = 100
            else:
                self.display_rate -= 1
        elif self.result_display_done:
            self.sudoku_grid[self.active_grid_posi[0]][self.active_grid_posi[1]].set_is_fade_in(False)
            self.gameover(0)
            self.result_display_done = False

        self.result_lock.release()

        
        return super().get_surface()



    def solve_sudoku(self):
        print('solve_sudoku:')
        self.result_lock.acquire()
        print(self.solve())
        self.result_lock.release()
        print(self.sudoku_data)
        print(self.result_sudoku_data)
    # 判断数度是否全部填充
    def is_completed(self):
        for row in self.sudoku_data:
            for data in row:
                if data == '.':
                    return False
        return True
    def set_grid(self, digit):
        # self.sudoku_grid[self.active_grid_posi[0]][self.active_grid_posi[1]].set_text(str(digit))
        
        if self.can_place(row=self.active_grid_posi[0], col=self.active_grid_posi[1], ch=digit):
            if self.is_completed():
                self.gameover(0)
        else:
            self.gameover(1)
        
        self.sudoku_data[self.active_grid_posi[0]][self.active_grid_posi[1]] = str(digit)
    
    # 激活鼠标点击到的方格，方便响应键盘事件
    def response_mouse_down(self,pos , mouse_index = 0):
        if self.running:
            for i  in range(9):
                for j in range(9):
                    if self.sudoku_grid[i][j].can_response(pos):
                        self.sudoku_grid[self.active_grid_posi[0]][self.active_grid_posi[1]].set_bgcolor(self.grid_color)
                        self.active_grid_posi = (i, j)
                        self.sudoku_grid[self.active_grid_posi[0]][self.active_grid_posi[1]].set_bgcolor(self.active_grid_color)
                        # self.active_grid = self.active_grid_color
                        return True
        return False
        # 响应键盘事件，当前激活的格子显示键盘输入字符，键盘只能输入1-9数字
        # 按键0-49  按键9-57
    def response_key_down(self, key):
        if self.running:
            tmp_key = key - 48
            if 1 <=tmp_key <= 9:
                self.set_grid(str(tmp_key))
                return True
        # print(key)
        return False

class ScoreBoard(AbstractScoreBoard):
    def __init__(self, main_game):
        super().__init__(main_game)
        r, g, b = abs(self.color[0]-10), abs(self.color[1]-10), abs(self.color[2]-10)
        self.control_button_color = (r, g, b)
        self.set_item_label(1, 'Reset')
        self.set_item_value(1, 'Solve')
        self.set_item_color(self.control_button_color,index= 1)

    # def can_response(self, pos):
    #     for item in self.items[1]:
    #         if item.can_response(pos):
    #             return True
    #     return False
        
    # 当点击reset / solve 按钮时的处理方法
    def response_mouse_down(self,pos , mouse_index = 0):
        if self.main_game.running:
            if self.items[1][0].can_response(pos):
                self.main_game.reset_game()
                self.main_game.start_game()
                return True
            elif self.items[1][1].can_response(pos):
                self.main_game.solve_sudoku()
                return True
            return False

    

