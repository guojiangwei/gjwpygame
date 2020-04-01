import pygame
import sys
import time
from PIL import Image
class RussianBox(object):
    def __init__(self, surface):
        self.surface = surface
        self.width = 20
        self.x = 0
        self.y = 0
        self.center = [10, 40]
        self.animate_status = False
        self.start = 255
        self.step = 3
        self.surs = []
        self.fps_clock = pygame.time.Clock()
        self.box_colors = (255,155,200)
        self.draw_surface()
        self.update()
    def update(self):
        i = 0
        self.surface.fill(self.box_colors)
        if self.animate_status:
            self.animate()
        else:
            for s, r in self.surs:
                print("before rotate: left=%d top=%d"%(r.left, r.top ))
                print("i=%d left=%d top=%d"%(i, r.left, r.top ))
                s.fill((0,100+ 50*(i),0))
                i += 1
                self.surface.blit(s, r)
                pygame.draw.rect(s,(255, 0, 230),((x,y),(self.width,self.width)),1)
    def animate(self):
        if self.start == 0 or self.start == 255:
            self.step = -self.step

        self.start += self.step
        alpha = self.start 
        i = 0
        self.surface.fill(self.box_colors)
        for s, r in self.surs:
            s= s.convert_alpha()
            
            s.fill((0,100+ 50*(i),0, alpha))
            i += 1
            # s.set_alpha(alpha)
            self.surface.blit(s, r)
            
            pygame.draw.rect(s,(255, 0, 230),((x,y),(self.width,self.width)),1)

    def set_animate(self, value):
        self.animate_status = value
    def draw_surface(self):
        width = self.width
        for i in range(4):
            surface2 = pygame.Surface((width,width))
            surface2.fill((0,100+50*i,0))
            rect = surface2.get_rect()
            rect.top = i * width
            self.surs.append([surface2, rect])

        
    def rotate(self):
        angle = 90

        # print("cx=%d cy=%d"%(self.center[0], self.center[1]))
        for s, r in self.surs:
            
            tmp = r.left
            r.left = -(r.top + 20 - self.center[1]) + self.center[0]
            r.top = (tmp - self.center[0]) + self.center[1]
        self.update()
    
    def translate(self, direction = [0,1]):
        for s,r in self.surs:
            r.left += direction[0]
            r.top += direction[1]
        self.center[0] += direction[0]
        self.center[1] += direction[1]
        self.update()

class TifGenerator(object):
    def __init__(self, surface, frequency = 1):
        self.frame_rate = frequency
        self.images = []
        self.count = 0
        self.surface = surface

    def set_frame_rate(self, rate):
        self.frame_rate = rate

    def generate_frame(self):
        self.count += 1
         
        if self.count == self.frame_rate :
            self.count = 0
            array = pygame.surfarray.array3d(surface2)
            image = Image.fromarray(array)
            self.images.append(image)

    def save(self,path=''):
        if path == '':
            # Image.
            self.images[0].save("test.gif", save_all = True, append_images = self.images, duration= [100]*(len(self.images)+1))
        else:
            self.images[0].save(paht+"test.gif",'GIF' ,save_all = True, append_images = self.images,optimize=False, duration= [1000]*len(self.images))


    



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    surface = pygame.Surface((600,600))
    colors = (255,155,200)
    surface2 = pygame.Surface((80,80))

    screen.fill((255,255,255), screen.get_rect())
    x = 0
    y = 0

    rect = surface.get_rect()
    rect2 = surface2.get_rect()
    boxes = RussianBox(surface2)
    # ss = draw_surface(surface2)
    tif = TifGenerator(surface2,2)
    surface.fill(colors,surface.get_rect())
    
    
    while True:
        
        
        pygame.draw.rect(surface2,(255, 0, 230),((0,0),(80,80)),1)
        # surface.blit(surface, rect)
        
        surface.blit(surface2, rect2)
        boxes.animate()
        tif.generate_frame()
        
            # flag = False
        

        # surface.fill((255,255,255))
        # pygame.draw.rect(surface,(255, 0, 230), ((0, 0), (self._width, self._height)), 1)
        
        
        time.sleep(0.1)
        screen.blit(surface,rect)
        
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tif.save()
                
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                surface2.fill(colors)
                
                rect.width = rect.width + 10
                rect.height = rect.height + 10
                print(rect.width, rect.height)
                print(surface2.get_size() , id(surface2))
                # surface2 = pygame.transform.smoothscale(surface2,(rect.height, rect.width))
                # surface2 = pygame.transform.rotate(surface2, 90)
                rect2 = surface2.get_rect()
                x +=10
                y +=10
                boxes.rotate()
                # array = []
                
                # image.save("test.jpeg")
                # print(len(array), len(array[0]) , type(array))
                # pygame.pixelcopy.surface_to_array(array, surface2, kind='P')
                # print(array)
            elif event.type == pygame.KEYDOWN:
                print(event.key, pygame.K_LEFT)
                if event.key == pygame.K_LEFT:
                    boxes.translate([-10,0])
                elif event.key == pygame.K_RIGHT:
                    boxes.translate([10,0])
                elif event.key == pygame.K_DOWN:
                    boxes.translate([0,10])
                elif event.key == pygame.K_UP:
                    print('ok')
                    boxes.translate([0,-10])
                # surface2 = pygame.Surface((rect.width,rect.height))
                # pygame.transform.




