import pygame
import random
import math
try:
    
    highscore = open("HIGHSCORE_FOR_SNAKE","r")
    highscore.close()
except:
    highscore = open("HIGHSCORE_FOR_SNAKE","x")
    highscore.close()
pygame.init()
BIGNESS = 1
wn = pygame.display.set_mode((1500,750))
def refill():
    wn.fill((0,0,0))



class PARTICLES(object):
    def __init__(self,choicecolors):
        self.x = random.randint(-1000,1000)
        self.y = random.randint(-1000,1000)
        self.radius = 3
        
        self.color = random.choice(choicecolors)
    def draw(self):
        pygame.draw.circle(wn,self.color,(int(self.x),int(self.y)),self.radius)
        
    def check(self):
        t1 = circles[0]
        t2 = self
        distance = math.sqrt(math.pow(t1.x-t2.x,2)+math.pow(t1.y-t2.y,2))
        if distance<self.radius+t1.radius:
            circles.append(CIRC(len(circles)))
            highscorenumber = open("HIGHSCORE_FOR_SNAKE","r")
            highscorenum = highscorenumber.read()
            highscorenumber.close()
            try:
                if int(highscorenum)<int(len(circles)):
                    highscore = open("HIGHSCORE_FOR_SNAKE","w")
                    highscore.write(str(len(circles)))
                    highscore.close()
            except:
                highscore = open("HIGHSCORE_FOR_SNAKE","w")
                highscore.write(str(len(circles)))
                highscore.close()
            colors.append(random.choice(choicecolors))
            self.x = random.randint(-1000,1000)
            self.y = random.randint(-1000,1000)
class CIRC(object):
    def __init__(self,num):
        self.num = num
        self.speed = 3
        self.orispeed = self.speed
        self.dis = 0
        if self.num == 0:
            
            self.x = int(1500//2)
            self.y = int(750//2)
        else:
            self.x = circles[self.num-1].x+self.dis
            self.y = 370
            
        self.radius = 8
        self.oriradius = self.radius
        self.inc = 30
        self.before_speed = 0
    def draw(self):
        pygame.draw.circle(wn,colors[self.num],(int(self.x),int(self.y)),self.radius)
        self.radius = len(circles)//self.inc + self.oriradius
            
    def move(self):
        '''keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and len(circles)!=1:
            self.speed = 6
            
            
        else:
            self.speed = self.orispeed'''
        self.x = circles[0].x
        self.y = circles[0].y
        slope_x = pygame.mouse.get_pos()[0] - circles[0].x
        slope_y = pygame.mouse.get_pos()[1] - circles[0].y
        
        distance = math.sqrt(math.pow(self.x-pygame.mouse.get_pos()[0],2)+math.pow(self.y-pygame.mouse.get_pos()[1],2))
        find_speed = distance/self.speed
        if find_speed == 0:
            find_speed = self.before_speed
        else:
            self.before_speed = find_speed
        self.x+=slope_x//find_speed
        self.y+=slope_y//find_speed
        for i in circles:
            i.x-=slope_x//find_speed
            i.y-=slope_y//find_speed
        for i in particles:
            i.x-=slope_x//find_speed
            i.y-=slope_y//find_speed
        
    





colors = []
choicecolors = ((0,128,128),(255,0,0),(0,255,0),(150,75,0),(255,255,0),(128,0,128),(230,230,250),(255,255,255),(127,255,0),(255,182,193),(255,69,0))
particles = []
for i in range(1000):
    particles.append(PARTICLES(choicecolors))
circles = []

for i in range(BIGNESS):
    
    circles.append(CIRC(i))
    colors.append(random.choice(choicecolors))



def snakedraw(circles):
    circles[-1].move()
    circles.insert(0, circles.pop(-1))
    
    for x in circles:
        x.draw()
        
        x.num+=1
    circles[0].num = 0
def draw():
    refill()
    for i in particles:
        i.draw()
        i.check()
    snakedraw(circles)
    
    highscorenumber = open("HIGHSCORE_FOR_SNAKE","r")
    highscorenum = highscorenumber.read()
    highscorenumber.close()
    
    font = pygame.font.Font("freesansbold.ttf",32)
    text = font.render("HIGHSCORE: "+str(highscorenum), True, (255,255,255),(0,0,0))
    recttext =(0, 0) 
    wn.blit(text, recttext)
run = True
while run:
    pygame.time.delay(5)
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    pygame.display.update()




    
pygame.quit()
