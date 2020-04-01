import pygame

import random
import pygame
from mygame_framework import *
import os
from settings  import Settings

class MainRussiaBox(AbstractGame):
    def __init__(self, main_game):
        super().__init__(main_game)
       
        # self.level = 1
        self.box_size = 25
        self.game_panel = RussiaBox(self)
        self.sb = ScoreBoard(self)
        self.game_name = 'RussiaBox'
        self.main_window.add_main(self.game_panel)
        
        main_game.main_window.register_key_down(self.game_panel)


        self.game_result = GameResult(self)
        self.main_window.add_main(self.game_result)
        self.main_window.register_mouse_down(self.game_result)

        self.set_active(False)
        
    def start_game(self):
        print("start Russia box!")
        super().start_game()
        self.set_preview(self.game_panel.next_shape)
    
    def set_preview(self,shape):
        left,top = shape.start_position
        preview_shapes = [(s[0]-left, s[1]-top) for s in shape.shapes]
        self.sb.set_preview(preview_shapes, shape.color)
        

class Box(Button):
    def __init__(self,row = 0, col = 0, x = 0,y = 0, height = 20, width = 20,  background_color = (255, 255, 255)):
        super(Box,self).__init__(x = x, y = y, height = height, width = width,  background_color = background_color)
        self.row = row
        self.col = col
        self.set_border_color((0,100,100))

###step:
# 1, init a shape randomly   falled from top to bottom
# 2, generating a  shape then show it  on the  score board 
# 3, another shape genereated by above  fall from top to bottom when current shape fall to the bottom
# 4, examin how many scores you have , show the score to score board
# 5, loop from step 2  until game over
###
class RussiaBox(AbstractGamePanel):
    def __init__(self, main_russia_box, level=1):
        
        self.size = main_russia_box.box_size
        self.box_color = (0,0,100)
        self._rows = 20
        self._cols = 10
        self._max_rows = 20
        self._max_cols = 10
        self.refresh_rate = 10000 # update box every 1 second
        self.refresh_time = 0

        super(RussiaBox,self).__init__( main_game=main_russia_box,height=main_russia_box.box_size * self._max_rows + 2,width=main_russia_box.box_size * self._max_cols + 2)
        self.init_graph_grid()

        
    def init_graph_grid(self):
        
        self.graph_boxes = [  [] for _ in range(self._max_rows) ]
        for i in range(self._max_rows):
            for j in range(self._max_cols):
                button = Box(row = i, col=j,x=j * self.size, y=i * self.size,
                height=self.size, width=self.size,
                 background_color= self.box_color)
                self.graph_boxes[i].append(button)
                self.add(button)
                
        
    def reset_game(self):
        super().reset_game()
        print("reset russia box")
        
        self.box_status = [  [ 0 for _ in range(self._max_cols)] for _ in range(self._max_rows) ]
        self.current_shape = self.generate_box_shape()
        self.next_shape = self.generate_box_shape()

    
    def get_surface(self):
        if self.running:
            # print("russia box is started!")
            if self.refresh_time % self.refresh_rate == 0:
                self.refresh_time = 0
                self.shape_fall_down()
            self.refresh_time += Settings.REFRESH_RATE
            
        return super().get_surface()

# generate a box shape randomly depends on shape type 
    def shape_fall_down(self):
        def can_fall_down():
            for p in self.current_shape.shapes:
                tmp = p[1] + 1
                if tmp < 0 or tmp >= self._rows or self.box_status[tmp][p[0]] == 1:
                    return False
            return True
        
        if can_fall_down():
            self.update_boxes_graph(self.box_color)
            self.current_shape.fall_down()
            self.update_boxes_graph(self.current_shape.color)
        else:
            self.update_boxes_status()
            tmp_score = self.compute_score()
            print("score:",tmp_score)
            if tmp_score != 0:
                self.set_score(self.score + tmp_score)
                self.eliminate_row()
            # self.update_boxes_status()
            if self.is_over(self.next_shape):
                self.gameover(0)

            else:
                self.current_shape = self.next_shape       
                self.next_shape = self.generate_box_shape()
                self.set_preview(self.next_shape)
    # determin if the game can be continued
    def is_over(self, shape):
        for p in shape.shapes:
            if self.box_status[p[1]][p[0]] == 1:
                return True
        return False

    def update_boxes_status(self):
        for shape in self.current_shape.shapes:
            self.box_status[shape[1]][shape[0]] = 1
    def set_preview(self, boxshapes):
        self.main_game.set_preview(boxshapes)

    def update_boxes_graph(self, color):
        # print('update_boxes_graph:boxesrows=%d  boxescols=%d '%(len(self.graph_boxes), len(self.graph_boxes[0])))
        for box in self.current_shape.shapes:
            self.graph_boxes[box[1]][box[0]].set_bgcolor(color)


# eliminate the row filled with -1
    def eliminate_row(self):
        print("eliminating a row that all value is 0")
        print(self.current_shape.shapes)
        step = 1
        for p in self.current_shape.shapes:
            row = p[1]
            if not (1 in self.box_status[row]) :
                if row > 0:
                    for r in range(row - 1, 0,-1 ):
                        if  (-1 in self.box_status[r]) :
                            step += 1
                            continue
                        for c in range(self._max_cols):
                            self.box_status[r+step][c] = self.box_status[r][c]
                            self.graph_boxes[r+step][c].set_bgcolor(self.graph_boxes[r][c].get_bgcolor())
                else:
                    for b in self.graph_boxes[row]:
                        b.set_bgcolor(self.box_color)

    # compute how many points you have get
    def compute_score(self):
        row_count = 0
        for p in self.current_shape.shapes:
            row = p[1]
            if not (0 in self.box_status[row]):
                self.box_status[row] = [-1]*len(self.box_status[row])  
                row_count += 1
        if row_count == 0:
            return 0
        elif row_count <= 2:
            return 100*row_count
        elif row_count == 3:
            return 400
        else:
            return 800
        

    
    def response_key_down(self, key):
        if self.running:
            if key == pygame.K_LEFT:
                self.shape_translation(-1)
                return True
            elif key == pygame.K_RIGHT:
                self.shape_translation(1)
                return True
            elif key == pygame.K_DOWN:
                pass
            elif key == pygame.K_UP:
                self.shape_rotate()
                return True
        return False
    def shape_rotate(self):
        def can_rotate():
            for p in self.current_shape.shapes:
                tmp = p[0]
                xi = -(p[1] - self.current_shape.center_top) + self.current_shape.center_left
                yi = p[0] - self.current_shape.center_left + self.current_shape.center_top
                if xi >= 10 or  xi < 0 or yi < 0 or yi >= 20 :
                    return False
            return True
        if can_rotate():
            self.update_boxes_graph(self.box_color)
            self.current_shape.rotate()
            self.update_boxes_graph(self.current_shape.color)
        
    def shape_translation(self, direction=1):
        def can_translate(direction):
            for p in self.current_shape.shapes:
                tmp = p[0] + direction
                if tmp < 0 or tmp >= 10 or self.box_status[p[1]][tmp] == 1:
                    return False
            return True
        if can_translate(direction):
            self.update_boxes_graph(self.box_color)
            self.current_shape.translate(direction)
            self.update_boxes_graph(self.current_shape.color)
    def generate_box_shape(self): 
        shape = BoxShapes(type=random.choice(BoxShapes.SHAPE_TYPE)) 
        # for s in shape.shapes:
        return shape


    
class ScoreBoard(AbstractScoreBoard):
    def __init__(self,main_game):
        super().__init__(main_game)
        # create a preview  panel for shape
        xm = self.center_x
        ym = self.center_y
        self.preview = [[] for _ in range(4) ]

        for i in range(4):
            for j in range(4):
                tmp_b = Button(x=xm - 30 + 15*i,y=ym-30+15*j, width=15, height=15,background_color=self.color)
                self.preview[i].append(tmp_b)
                self.add(tmp_b)
        
        self.set_item_label(1, 'time')
        
    
    def init(self):
        for pl in self.preview:
            for p in pl:
                p.set_bgcolor(self.color)

    def set_active(self, value):
        super().set_active(value)
        for pl in self.preview:
            for p in pl:
                p.set_visible(value)
    

    def set_preview(self, pres, color):
        self.init()
        for p in pres:
            self.preview[p[0]][p[1]].set_bgcolor(color)
    def set_time_label(self, time):
        self.set_item_value(1, time)


class BoxShapes(object):
    """ There are seven types of shape in this game,each shape is consisted of four boxes
    and has different colors
    """
    SHAPE_TYPE = [0,1,2,3,4,5,6]
    COLORS = [(0x11,0xEE,0xEE),(0x09,0x38,0xF7),
        (0xF7,0x97,0x09),(0xFF,0xFF,0),
        (0x2B, 0xD5, 0x2B), (0xCC, 0x00, 0xFF),
        (0xFF,0,0)]
    def __init__(self, type = 0):
        self.shapes = []
        self.shape_type = BoxShapes.SHAPE_TYPE[type]
        self.start_position = [5, 0]
        self.box_amount = 4
        self.center_top = None
        self.center_left = None
        self.color = BoxShapes.COLORS[type]

        self.generate_shape(self.shape_type)

    def fall_down(self):
        for p in self.shapes:
            p[1] += 1
        self.center_top += 1

    def rotate(self):
        for p in self.shapes:
            tmp = p[0]
            p[0] = -(p[1] - self.center_top) + self.center_left
            p[1] = tmp - self.center_left + self.center_top

    def translate(self, direction=1):
        for p in self.shapes:
            p[0] += direction
        self.center_left += direction

    
    def generate_shape(self, type):
        if type == BoxShapes.SHAPE_TYPE[0]:
            for i in range(self.box_amount):
                # .... shape
                self.shapes.append([self.start_position[0], self.start_position[1]+i])
            self.center_top = self.start_position[1] + 2
            self.center_left = self.start_position[0]
        elif type == BoxShapes.SHAPE_TYPE[1]:
            self.shapes.append([self.start_position[0], self.start_position[1]])
            self.shapes.append([self.start_position[0], self.start_position[1]+1])
            self.shapes.append([self.start_position[0]+1, self.start_position[1]+1])
            self.shapes.append([self.start_position[0]+2, self.start_position[1]+1])
            self.center_top = self.start_position[1] + 1
            self.center_left = self.start_position[0] + 2
        elif type == BoxShapes.SHAPE_TYPE[2]:
            self.shapes.append([self.start_position[0], self.start_position[1] + 1])
            self.shapes.append([self.start_position[0] + 1, self.start_position[1] + 1])
            self.shapes.append([self.start_position[0]+2, self.start_position[1]+1])
            self.shapes.append([self.start_position[0]+2, self.start_position[1]])
            self.center_top = self.start_position[1] + 1
            self.center_left = self.start_position[0] + 2
        elif type == BoxShapes.SHAPE_TYPE[3]:
            self.shapes.append([self.start_position[0], self.start_position[1] ])
            self.shapes.append([self.start_position[0] , self.start_position[1] + 1])
            self.shapes.append([self.start_position[0] + 1, self.start_position[1]+1])
            self.shapes.append([self.start_position[0] + 1, self.start_position[1]])
            self.center_top = self.start_position[1] + 1
            self.center_left = self.start_position[0] + 1
        elif type == BoxShapes.SHAPE_TYPE[4]:
            self.shapes.append([self.start_position[0], self.start_position[1] + 1])
            self.shapes.append([self.start_position[0] + 1 , self.start_position[1] + 1])
            self.shapes.append([self.start_position[0] + 1, self.start_position[1]])
            self.shapes.append([self.start_position[0] + 2, self.start_position[1]])
            self.center_top = self.start_position[1] + 1
            self.center_left = self.start_position[0] + 1
        elif type == BoxShapes.SHAPE_TYPE[5]:
            self.shapes.append([self.start_position[0], self.start_position[1]])
            self.shapes.append([self.start_position[0] + 1 , self.start_position[1] + 1])
            self.shapes.append([self.start_position[0] + 1, self.start_position[1]])
            self.shapes.append([self.start_position[0] + 2, self.start_position[1] + 1])
            self.center_top = self.start_position[1] + 1
            self.center_left = self.start_position[0] + 1
        elif type == BoxShapes.SHAPE_TYPE[6]:
            self.shapes.append([self.start_position[0], self.start_position[1] + 1])
            self.shapes.append([self.start_position[0] + 1 , self.start_position[1] + 1])
            self.shapes.append([self.start_position[0] + 1, self.start_position[1]])
            self.shapes.append([self.start_position[0] + 2, self.start_position[1] + 1])
            self.center_top = self.start_position[1] + 1
            self.center_left = self.start_position[0] + 1






    
