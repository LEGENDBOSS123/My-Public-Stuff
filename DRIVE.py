    #  change x and y to adjust width and height of the screen.
x=1500
y=750


import pygame
import math
import random


pygame.init()



BG = (100,100,100)

wn = pygame.display.set_mode((x,y))

class DRIVER():
    def __init__(self):
        

        self.x = x//2
        self.y = y//2

        self.height = 25
        self.width = 10
        
        self.x_vel = 0
        self.y_vel = 0
        
        self.angle = 0
        self.angle_speed = 3
        
        self.speed = 0.03

        self.speed_limit = 5

        self.image = pygame.Surface((self.width,self.height))
        self.image.set_colorkey(BG)
        self.image.fill((255,255,255))

        self.rotated_image = pygame.transform.rotate(self.image,self.angle)

        self.rect = self.rotated_image.get_rect()
        self.rect.center = (self.x,self.y)
        
    def RESTART(self):
        
        DRIVER.x = x//2
        DRIVER.y = y//2
        DRIVER.GAME_OVER = False
        DRIVER.x_vel = 0
        DRIVER.y_vel = 0
        
    def MOVE(self):

        if self.angle<0:
            self.angle+=360
        if self.angle>=360:
            self.angle-=360

        if self.angle == 0:
            self.y_vel-=self.speed
        elif self.angle == 180:
            self.y_vel+=self.speed
        elif self.angle == 90:
            self.x_vel-=self.speed
        elif self.angle == 270:
            self.x_vel+=self.speed
        else:
            self.x_vel-=math.sin(math.radians(self.angle))*self.speed
            self.y_vel-=math.cos(math.radians(self.angle))*self.speed

        if self.y_vel > self.speed_limit:
            self.y_vel = self.speed_limit
        if self.y_vel < -self.speed_limit:
            self.y_vel = -self.speed_limit
        if self.x_vel > self.speed_limit:
            self.x_vel = self.speed_limit
        if self.x_vel < -self.speed_limit:
            self.x_vel = -self.speed_limit

        self.x+=self.x_vel
        self.y+=self.y_vel
        limit = 25
        if self.x<limit:
            self.x = limit
            self.x_vel = 0
        if self.x>x-limit:
            self.x = x-limit
            self.x_vel = 0
        if self.y<limit:
            self.y = limit
            self.y_vel = 0
        if self.y>y-limit:
            self.y = y-limit
            self.y_vel = 0

        
    def UPDATE(self):
        self.x_vel/=1.01
        self.y_vel/=1.01
        self.MOVE()
        
        self.image = pygame.Surface((self.width,self.height))
        self.image.set_colorkey(BG)
        self.image.fill((255,255,255))

        self.rotated_image = pygame.transform.rotate(self.image,self.angle)

        self.rect = self.rotated_image.get_rect()
        self.rect.center = (self.x,self.y)
        
    def KEY_CHECK(self):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.angle-=self.angle_speed
            
        if keys[pygame.K_LEFT]:
            self.angle+=self.angle_speed
        
    def DRAW(self):
        
        self.KEY_CHECK()
        
        self.UPDATE()

        wn.blit(self.rotated_image,self.rect)

class MAP():
    def __init__(self):
        
        self.x = x//2
        self.y = y//2
        
        self.obstacles = []
        self.portal = []
        self.lvl = 1
        self.start_balls = 5
        self.radius = 20
        
    def SET_UP(self):
        self.obstacles = []
        for i in range((self.lvl-1)*self.start_balls+self.start_balls-1):
            xy = (random.randint(-self.x,self.x),random.randint(-self.y,self.y))
            box = 100
            while xy[0]>-box and xy[0]<+box and xy[1]>-box and xy[1]<+box:
                xy = (random.randint(-self.x,self.x),random.randint(-self.y,self.y))

            self.obstacles.append(xy)
        self.portal = []
        self.portal.append((random.randint(-self.x,self.x),random.randint(-self.y,self.y)))

    def COLLISION(self,DRIVER,o,enemy):

        cx = math.cos(DRIVER.angle*math.pi/180) * (o[0]-DRIVER.x) - math.sin(DRIVER.angle*math.pi/180) * (o[1]-DRIVER.y) + DRIVER.x
        cy = math.sin(DRIVER.angle*math.pi/180) * (o[0]-DRIVER.x) + math.cos(DRIVER.angle*math.pi/180) * (o[1]-DRIVER.y) + DRIVER.y
    
        closex = 0
        closey = 0
        
        if cx < DRIVER.x-DRIVER.width//2:
            closex = DRIVER.x-DRIVER.width//2
            
        elif cx > DRIVER.x+DRIVER.width//2:
            closex = DRIVER.x+DRIVER.width//2
            
        else:
            closex = cx


        if cy < DRIVER.y-DRIVER.height//2:
            closey = DRIVER.y-DRIVER.height//2
            
        elif cy > DRIVER.y+DRIVER.height//2:
            closey = DRIVER.y+DRIVER.height//2
            
        else:
            closey = cy

        dis = math.sqrt( (cx-closex)**2 + (cy-closey)**2 )
        
        if dis <= self.radius:
            if enemy == True:
                
                DRIVER.RESTART()
            else:
                self.lvl+=1
                self.SET_UP()
                DRIVER.RESTART()
        
    def DRAW(self,DRIVER):
        #self.x-=DRIVER.x_vel
        #self.y-=DRIVER.y_vel
        for o in self.portal:
            self.COLLISION(DRIVER,(self.x+o[0],self.y+o[1]),False)
            pygame.draw.circle(wn,(0,0,200),(int(self.x+o[0]),int(self.y+o[1])),self.radius)
        for o in self.obstacles:
            self.COLLISION(DRIVER,(self.x+o[0],self.y+o[1]),True)
            pygame.draw.circle(wn,(200,0,0),(int(self.x+o[0]),int(self.y+o[1])),self.radius)
        
        

DRIVER = DRIVER()
MAP = MAP()
MAP.SET_UP()
def draw():
    
    wn.fill(BG)

    DRIVER.DRAW()

    MAP.DRAW(DRIVER)

run = True

while run:
    
    pygame.time.delay(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    draw()
    
    pygame.display.update()

    
pygame.quit()
