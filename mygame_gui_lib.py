import pygame
import pygame.font
import math
class AbstractPanel:
    def __init__(self,x = 0,y = 0, height = 10, width = 10, image = '', text = '', text_color = (0, 0, 0), background_color = (255, 255, 255)):
        self._x = int(x)
        self._y = int(y)
        self._image = image
        
        self.abs_x=0
        self._changed = False
        self.abs_y = 0
        self._background_color = background_color
        self._height = int(height)
        self._width = int(width)

        self._text = text
        self._text_color = text_color
        self._text_size = self._height - 8

        
        self.parent = None
        self.active = True
        self._visible = True
        self.alpha = 255
        self.alpha_step = 2
        self._border_color =tuple( abs(c - 20) for c in background_color  ) 
        
        sur = pygame.Surface((self._width,self._height))
        self.surface = sur.convert()
        # self.surface.fill(self._background_color)
        # self._set_surface()
        self.reset()
    
    def reset(self):
        self.alpha = 255
        self.surface.set_alpha(self.alpha)
        self.surface.fill(self._background_color)
        self._set_rect()
        self._set_content()
        self.draw_border()
        self._changed = False
    
    # 设置绝对坐标系
    def set_orginal(self, p_x, p_y):
        self.abs_x = p_x 
        self.abs_y = p_y 

    def set_bgcolor(self, color):
        self._background_color = color
        self._changed = True

    def set_text_size(self, size):
        self._text_size = size
        self._changed = True
        
    
    def get_bgcolor(self):
        return self._background_color
        
    def _process_text(self):
        self._font = pygame.font.SysFont(pygame.font.get_fonts()[3], self._text_size)
        text_surface = self._font.render(self._text, True, self._text_color, self._background_color)
        rect = text_surface.get_rect()
        rect.top = (self._height - rect.height)/2
        rect.left = (self._width - rect.width) / 2
        
        self.surface.blit(text_surface, rect)
        # self._set_rect()
        # print(self._text)
    def _process_image(self):
        image_surface = pygame.transform.smoothscale(pygame.image.load(self._image), (self._height, self._width))
        self.surface.blit(image_surface, image_surface.get_rect())
    def set_visible(self, status):
        # if not status:
        self._visible = status
        self.active = status
        self._changed = True

    def get_visible(self):
        return self._visible

    def _set_rect(self):
        # self.surface = pygame.transform.smoothscale(self.surface,(self._height, self._width))
        # self.rect = self.surface.get_rect()
        if self.surface.get_rect().width != self._width and self.surface.get_rect().height != self._height:
            self.surface = pygame.transform.smoothscale(self.surface,(self._width, self._height))
        self.rect = self.surface.get_rect()
        self.rect.left = self._x
        self.rect.top = self._y
        self._width = self.rect.width
        self._height = self.rect.height

    def set_position(self, x, y):
        self._x = x
        self._y = y
        # print(self._x , self._y)
        # self._set_rect()
        self.rect.left = self._x
        self.rect.top = self._y
        self._changed = True
    def get_width(self):
        return self._width
    def get_height(self):
        return self._height
    def set_width(self, width):
        self._width = int(width)
        self.rect.width = self._width
        self._changed = True
        
    def set_height(self, height):
        self._height = int(height)
        self.rect.height = self._height
        self._text_size = self._height - 8
        self._changed = True
    def set_rect(self, pos= (0, 0),size = (0, 0)):
        self._x = pos[0]
        self._y = pos[1]
        self.rect.left = pos[0]
        self.rect.top = pos[1]

        self._height = size[1]
        self.rect.height = size[1]
        self._width = size[0]
        self.rect.width = size[0]

        # pygame.transform.smoothscale(self.surface)

        self._changed = True
    def draw_border(self):
        # color = self.get_bgcolor()
        # color = tuple( abs(c - 30) for c in color  )
        pygame.draw.rect(self.surface, self._border_color, ((0, 0), (self._width, self._height)), 1)
    
    def set_border_color(self, color):
        self._border_color = color
        self.reset()
    
        
    def _set_content(self):
        
        if self._image != '':
            self._process_image()
            return
            
        if self._text != '':
            self._process_text()
            return
        
    def get_surface(self):
        if self._changed:
            self.reset()
        
        return self.surface, self.rect

    def contain_point(self, point):
        return self.rect.collidepoint(point)
    def can_response(self, pos):
        pos = self._convert_to_relatepos(pos)
        # print(pos)
        return self.active and self.contain_point(pos)
    def _convert_to_relatepos(self, pos):
        
        return (pos[0] - self.abs_x ,pos[1] - self.abs_y)
    
    def setParent(self, p):
        self.parent = p

# 按钮渐入渐出效果
    def fade_in(self):
        self.surface.set_alpha(self.alpha)
        self.alpha += self.alpha_step
        if self.alpha >= 255:
            self.alpha = 255
            self.alpha_step = -self.alpha_step
        elif self.alpha <= 0:
            self.alpha = 0
            self.alpha_step = -self.alpha_step
        


class Panel(AbstractPanel):
    def __init__(self, x = 0,y = 0, height = 10, width = 10, image = '', text = '', text_color = (0, 0, 0), background_color = (255, 255, 255)):
        super(Panel, self).__init__(x = x, y = y, height = height, width = width, image = image, text = text, text_color = text_color, background_color = background_color)
        self.elements = []
        self.rect.left = x
        self.rect.top = y

        self.count = 0
        
    
    
    def set_orginal(self, p_x, p_y):
        super().set_orginal(p_x, p_y)
        for elem in self.elements:
            elem.set_orginal(self.abs_x + self._x, self.abs_y + self._y)

    def add(self, elem):
        if elem:
            self.elements.append(elem)
            elem.set_orginal(self.abs_x + self._x, self.abs_y + self._y)
            # elem.abs_x = self.abs_x 
            # elem.abs_y = self.abs_y
            elem.setParent(self)

    def add_to_center(self,elem):
        width = elem.get_width()
        height = elem.get_height()
        x = (self._width  - width)/2
        y = (self._height -height )/2
        elem.set_position(x, y)
        self.add(elem)
    
    def get_surface(self):
        if self._changed:
            self._changed = False
        # self.surface.fill(self._background_color)
        # self.surface.set_clip()
            self.reset()
        self.blit_elems()
        # self.draw_border()
        return self.surface, self.rect
        # return super().get_surface()
    
    def blit_elems(self):   
        # self.surface.fill(self._background_color)     
        for elem in self.elements:
            if elem.get_visible():
                sur, rect = elem.get_surface()
                self.surface.blit(sur, rect)


class Button(AbstractPanel):
    def __init__(self,x = 0,y = 0, height = 30, width = 60, image = '', text = '', text_color = (0, 0, 0), background_color = (255, 255, 255)):
        super(Button, self).__init__(x = x, y = y, height = height, width = width, image = image, text = text, text_color = text_color, background_color = background_color)
        
        # self.surface, self.rect = self.get_surface()
        # self.rect = self.surface.get_rect()
        
        # self._set_rect()
        # self.draw_border()
        
        
    
    def set_x(self, x):
        self.rect.left = x
        self._x = self.rect.left

    def set_right(self, x = 0):
        if self.parent:
            x = self.parent.get_width() + x - self._width
        self.set_x(x)
            
        # self._set_rect()
    def get_text(self):
        return self._text
    

    def set_text(self, text):
        self._text = text
        self._image = ''
        self._changed = True
        self._set_content()
    def set_image(self, path):
        self._text = ''
        self._image = path
        self._changed = True
        self._set_content()
    
class OptionButton(Panel):
    def __init__(self, values ,x = 0,y = 0, height = 30, width = 60, text_color = (0, 0, 0), background_color = (255, 255, 255)):
        super(OptionButton, self).__init__(x = x, y = y, height = height, width = width, text_color = text_color, background_color = background_color)
        self._values = values
        self._texts = [str(t) for t in values ]
        self._item_count = len(values)
        self._items = []
        self.single_height = height/self._item_count
        self.single_width = (width-2)/2
        self.checked = [False for _ in range(self._item_count)]
        self.checked[0] = True
        self.current_value = self._values[0]
        self.generate_item()

    def set_visible(self, value):
        for item in self.elements:
            item.set_visible(value)
        for item in self._items:
            item.set_visible(value)
        super().set_visible(value)
    
    def generate_item(self):
        for i in range(self._item_count):
            left_button = Button(x= 0, y=i*self.single_height, width= self.single_width, height= self.single_height,background_color=self.get_bgcolor())
            self.add(left_button)
            self._items.append(left_button)
            right_button = Button(x= self.single_width, y=i*self.single_height, width= self.single_width, height= self.single_height, text=self._texts[i],background_color=self.get_bgcolor())
            self.add(right_button)
        self.draw_left_button()
            
    def draw_left_button(self):
        for i in range(self._item_count):
            if self.checked[i]:
                self.draw_hook(self._items[i])
            else:
                self.draw_circle(self._items[i])
    
    def draw_hook(self, item):
        item.reset()
        surface,rect = item.get_surface()
        color = (0, 0, 255)
        pygame.draw.line(surface,color,(item.get_width()/4, item.get_height()/2), (item.get_width()/2, item.get_height()),3)
        pygame.draw.line(surface,color,(item.get_width()/2, item.get_height()), (3*item.get_width()/4, item.get_height()/5),3)
        
    def draw_circle(self, item):
        item.reset()
        surface,rect = item.get_surface()
        color = (0, 0, 255)
        radius = int((self.single_height/2-1) if self.single_height < self.single_width else (self.single_width/2-1))
        pygame.draw.circle(surface,color,(int(item.get_width()/2), int(item.get_height()/2)),radius ,3)
        # pygame.draw.line(surface,color,((item.get_width()/2, item.get_height()), (3*item.get_width()/4, item.get_height()/5),3)
    
    def response_mouse_down(self,pos , mouse_index = 0):
        for i in range(self._item_count):
            if self._items[i].can_response(pos):
                # print("test option button!")
                self.checked[:] = [False for _ in range(self._item_count)]
                self.checked[i] = True
                self.draw_left_button()
                self.current_value = self._values[i]
                self.draw_left_button()
                return True
        return False


    

