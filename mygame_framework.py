import threading
import time
from mygame_gui_lib import Panel
from mygame_gui_lib import Button
# from mygame_gui_lib import GifGenerator
from settings import Settings
# 每个游戏点主要入口类都要实现自己点相关方法 并调用父类相关方法
class AbstractGame(object):
    def __init__(self, main_game_window):
        self.main_game_window = main_game_window 
        self.high = 0
        self.current_score = 0
        self.time = 0
        self.main_window = main_game_window.main_window
        self.running = False


# 子类中必须初始化以下变量
        self.sb = None
        self.game_panel = None
        self.game_result = None
        self.game_name = ''
        
        
    
    # def set_gif(self, active):
    #     self.game_panel.set_gif(active)
    # def get_gif(self):
    #     return self.game_panel.get_gif()

    # def save_gif(self):
    #     self.game_panel.save_gif(self.game_name)

    def get_refresh_rate(self):
        return Settings.REFRESH_RATE

# 设置游戏激活状态
    def set_active(self, value):
        self.game_panel.set_visible(value)
        self.sb.set_active(value)
        self.game_result.set_active(value)

# 重载游戏
    def reset_game(self):
        print("reset  game!")
        self.game_panel.reset_game()
        self.game_result.reset_result()
        self.sb.reset()
        self.time = 0
        self.running = False
        self.current_score = 0
        self.set_score(0)
        
# 开始游戏
    def start_game(self):
        self.reset_game()
        self.game_panel.start_panel()
        self.running = True
        t = threading.Thread(target= self.timer)
        t.start()
# 停止游戏
    def stop_game(self, status):
        print('stop game!')
        self.running = False
        self.game_panel.running = False
        self.game_result.set_status(status)

# 设置分数
    def set_score(self, score):
        self.sb.set_score(str(score))
    
    # 游戏计时
    def add_time(self):
        self.time += 1
        self.sb.set_time_label(str(self.time))

    # 计时器
    def timer(self):
        while self.running:
            time.sleep(1)
            self.add_time()
            
# 返回主体窗口
    def get_game_panel(self):
        return self.main_window.get_main()


# 每个游戏点主主界面必须继承这个类，并重载重置游戏/游戏结束/计算分数等方法
class AbstractGamePanel(Panel):
    def __init__(self,main_game,width = 10, height =10, level=1):
        super().__init__(x=5, y=5, height=height,width=width)
        self.score = 0
        self.running = False
        self.main_game = main_game
        self.active_gif = False
        # self.gif_frame_rate = 10
        # self.gif_frame_count = 0
        
        
        # self.reset_game()
    
    def get_surface(self):
        if self.active_gif:
            self.generate_frame()
        return super().get_surface()
    def start_panel(self):
        self.running = True
    def reset_game(self):
        # self.reset()
        # self.active_gif = False
        self.running = False

    def gameover(self, status):
        self.running = False
        # self.active_gif = False
        self.main_game.stop_game(status)

    def set_score(self,score):
        self.score = score
        self.main_game.set_score(score)
    
    # def set_gif(self, active):
    #     self.active_gif = active
    #     # self.game_panel.set_gif(active)
    # def get_gif(self):
    #     return self.active_gif
    # def save_gif(self,path):
    #     self.gif_gen.save(path)

# implement scoreboard
class AbstractScoreBoard:
    def __init__(self,main_game):
        self.main_game = main_game
        self.panel = main_game.main_window.get_right()
        self.center_x = self.panel.get_width()/2 - 5
        self.center_y = self.panel.get_height()/2 - 40

        
        ym = self.center_y
        xm = self.center_x

        
        #预留40像素放其他点组件
        self.height = 40
        self.color =  self.panel.get_bgcolor() #(200, 200, 200)
        self.items = []

        # 
        # self.gif_button = Button(x=xm//2, y=self.height , width= xm, height= self.height ,background_color=self.color, text='GIF')
        # self.add(self.gif_button)

        ym = ym + self.height
        for i in range(3):
            tmp_button1 = Button(x=2, y=ym + self.height * i, width= xm, height= self.height ,background_color=self.color)
            self.add(tmp_button1)
            tmp_button2 = Button(x=xm+3, y=ym + self.height * i, width= xm, height=self.height,background_color=self.color)
            self.add(tmp_button2)
            self.items.append((tmp_button1, tmp_button2))
            # ym = ym +height
        
        self.set_item_label(0,'High S')
        self.set_item_label(2,'score')
            
    
    
    def init(self):
        pass
    def reset(self):
        # self.items[1][1].set_text(str(0))
        self.items[2][1].set_text(str(0))
        self.init()

    def add(self, item):
        self.panel.add(item)
    
    # setting scoreboard state
    def set_active(self, value):
        for item in self.items:
            item[0].set_visible(value)
            item[1].set_visible(value)
    
    def set_item_label(self, index, text):
        self.items[index][0].set_text(str(text))

    def set_item_value(self, index, text):
        self.items[index][1].set_text(str(text))

    def get_item_value(self, index, text):
        return self.items[index][1].get_text()
    
    def set_score(self, score):
        self.set_item_value(2,str(score))

    def set_high_score(self, high):
        self.set_item_value(0,str(score))
    
    def set_item_color(self, color, index):
        self.items[index][0].set_bgcolor(color)
        self.items[index][1].set_bgcolor(color)

# 判断分数版面是否可以响应鼠标点击事件
    def can_response(self, pos):
        return self.panel.can_response(pos)



# 游戏成功或者失败点效果类
class GameResult(Panel):
    def __init__(self,game,text='Play Game!',width=150):
        height = 60
        super(GameResult, self).__init__(width=width,height=height*2)
        self.status_alpha = 0
        self.status_step = 1
        self.status_msg = ['congratulations!','You are failed!']
        self.button_text = ['Play again!', 'Play!']
        self.add(Button(x=0, y=0, width=width, height=height, background_color=(255,255,0)))
        self.elements[0].set_text_size(20)
        self.add(Button(x=0, y=height, text=self.button_text[1], width=width, height=height, background_color=(100,100,100)))
        self.elements[1].set_text_size(25)

        # self.elements[0].set_visible(False)
        self.game = game
        self.reset_result()

    def reset_result(self):
        self.elements[0].set_visible(False)
        self.elements[1].set_visible(True)
        self.elements[1].set_text(self.button_text[1])

    # def set_all_active(self, value):
    #     self.set_visible(value)
    #     for elem in self.elements:
    #         elem.set_visible(value)
    #         elem.set_visible(value)


    def set_active(self, value):
        self.set_visible(value)
        if value:
            self.elements[1].set_visible(value)
        else:
            for elem in self.elements:
                elem.set_visible(value)
                elem.set_visible(value)


    # def blit_elems(self):   
    #     self.surface.fill(self._background_color)     
    #     # print(self.elements)
    #     for i in range(len(self.elements)):
    #         if self.elements[i].get_visible():
    #             sur, rect = self.elements[i].get_surface()
    #             if i == 0:
    #                 self.elements[i].fade_in()
    #             self.surface.blit(sur, rect)

    def can_response(self, point):
        return self.elements[1].can_response(point)
    
    ### status=0 game success !
    #  status=1 game failed!  
    # status=2 pause game
    ###
    def set_status(self, status):
        print("game status:",status)
        self.set_visible(True)
        self.elements[0].set_visible(True)
        self.elements[0].set_is_fade_in(True)
        if status == 0:
            self.elements[0].set_text(self.status_msg[0])
            self.elements[1].set_text(self.button_text[0])
        elif status == 1:
            print(self.status_msg[1])
            self.elements[0].set_text(self.status_msg[1])
            self.elements[1].set_text(self.button_text[0])
    
    def response_mouse_down(self, pos, mouse_index=0):
        if self.get_visible():
            print("press on play button")
            self.set_active(False)
            self.game.start_game()
            return True
        return False