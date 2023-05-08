import pygame
import math
import random
import pickle


pygame.init()

p1 = "PLAYER 1"

p2 = "PLAYER 2"


get_points = 0
p1_color = (50,255,50)


get_points2 = 0
p2_color = (50,50,255)





xval = 1200
yval = 700
wn = pygame.display.set_mode((xval,yval))
def refill():
    wn.fill((75,75,75))
def refill2():
    r,g,b = random.randint(0,255),random.randint(0,255),random.randint(0,255)
    wn.fill((r,g,b))

class PARTICLES(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.range = 50
        self.big = 5
        self.count = 0
        self.directionx = random.randint(-1*self.range,self.range)
        self.directiony = random.randint(-1*self.range,self.range)

        while self.directionx==0:
            self.directionx = random.randint(-1*self.range,self.range)
        while self.directiony==0:
            self.directiony = random.randint(-1*self.range,self.range)
    def draw(self):

        pygame.draw.rect(wn,(255,255,0),(self.x,self.y,self.big,self.big))
        self.x+=self.directionx
        self.y+=self.directiony
        self.count+=1
    def check(self):
        global mapnum
        global p1
        global p2
        if self.count >=50:

            self.count = 0


            if player1.scoredead == True:
                player1.points+=1

                player1.scoredead = False
            elif player2.scoredead == True:
                player2.points+=1
                player2.scoredead = False
            
            mapnum+=1
            if mapnum == len(maps):
                mapnum = 0
            player1.spawn()
            player2.spawn()
            draw()
            pygame.display.update()
            pygame.time.delay(1000)







class PLATFORM(object):
    def __init__(self,x,y,shapesizex,shapesizey,color,bouncy,xrate,yrate,angle,until):
        self.x_until = until[0]
        self.y_until = until[1]
        self.angle = angle
        self.bouncy = bouncy
        self.o_xrate = xrate
        self.o_yrate = yrate

        self.xrate = xrate
        self.yrate = yrate
        self.rex = x
        self.rey = y
        self.x = x
        self.y = y
        self.shapesizex = shapesizex
        self.shapesizey = shapesizey
        self.platform = (self.x,self.y,self.shapesizex,self.shapesizey)
        self.color = color


        self.image_o = pygame.Surface((self.shapesizex,self.shapesizey))
        self.image_o.set_colorkey((75,75,75))
        self.image_o.fill(self.color)


        self.rect = self.image_o.get_rect()
        self.rect.center = (self.x+self.shapesizex//2,self.y+self.shapesizey//2)


    def draw(self):

        self.x+=self.xrate
        self.y+=self.yrate
        if self.x_until != None:
            if self.x>self.x_until and self.o_xrate>0:
                self.xrate*=-1
            if self.x<self.x_until and self.o_xrate<0:
                self.xrate*=-1


            if self.x==self.rex:
                self.xrate*=-1

        if self.y_until != None:
            if self.y>=self.y_until and self.o_yrate>0:
                self.yrate*=-1
            if self.y<=self.y_until and self.o_yrate<0:
                self.yrate*=-1
            if self.y==self.rey and self.yrate>0:
                self.yrate*=-1
            if self.y==self.rey and self.yrate<0:
                self.yrate*=-1
        oldcenter = self.rect.center


        self.platform = (self.x,self.y,self.shapesizex,self.shapesizey)
        #pygame.draw.rect(wn,self.color,self.platform)
        self.new_im = pygame.transform.rotate(self.image_o,self.angle)
        self.rect = self.new_im.get_rect()
        self.rect.center = (self.x+self.shapesizex//2,self.y+self.shapesizey//2)
        wn.blit(self.new_im , self.rect)





class PLAYER(object):
    def __init__(self,playernum,r):




        self.stay_dead = False

        self.playernum = playernum
        if self.playernum == 1:
            self.x = maps[mapnum][2][0]
            self.y = maps[mapnum][2][1]
        if self.playernum == 2:
            self.x = maps[mapnum][3][0]
            self.y = maps[mapnum][3][1]

        if self.playernum == 1:
            self.get_points = 0
            self.points = 0
            
        if self.playernum == 2:
            self.get_points = 0
            self.points = 0
            


        self.radius = r
        self.mass = r/4
        self.massmore = 2*self.mass
        self.massless = self.mass
        #x value related
        self.speed = 0
        self.deltaspeed = 0.3
        self.maxspeed = 12
        #y value related
        self.gravspeed = 0.4
        self.originalgravspeed = self.gravspeed
        self.holdit = -2.5
        self.originalholdit = self.holdit
        self.landed = False
        self.dead = False
        self.dead_only_once = False
        self.particles = []
        self.scoredead = False
        self.nochanges = True



    def write(self):
        font = pygame.font.Font("freesansbold.ttf",32)


        if self.playernum == 2:
            text = font.render(str(p2)+":"+str(self.points), True, p2_color,(75,75,75))
            recttext =(0, 32)
        if self.playernum == 1:
            text = font.render(str(p1)+":"+str(self.points), True, p1_color,(75,75,75))
            recttext =(0, 0)
        wn.blit(text, recttext)
    def spawn(self):

        if self.playernum == 1:
            self.x = maps[mapnum][2][0]
            self.y = maps[mapnum][2][1]
        if self.playernum == 2:
            self.x = maps[mapnum][3][0]
            self.y = maps[mapnum][3][1]


        #x value related
        self.speed = 0
        
        self.deltaspeed = 0.3
        self.maxspeed = 12
        #y value related
        self.gravspeed = 0.4
        self.originalgravspeed = self.gravspeed
        self.holdit = -2.5
        self.originalholdit = self.holdit
        self.landed = False
        self.dead = False
        self.dead_only_once = False
        self.nochanges = True
        self.particles = []
        if self.stay_dead == True:
            for i in maps[mapnum][0]:
                i.x = i.rex
                i.y = i.rey
                i.xrate = i.o_xrate
                i.yrate = i.o_yrate
            for i in maps[mapnum][1]:
                i.fillinradius = 0
                i.stop = False



            if self.playernum == 1:
                bullet1.x = player1.x
                bullet1.y = player1.y
                bullet1.aimx = 0
                bullet1.neg = -1
                bullet1.count = 0
                bullet1.shoot = False
                bullet1.pressed = False
                bullet1.change = True





            if self.playernum == 2:
                bullet2.x = player2.x
                bullet2.y = player2.y
                bullet2.aimx = 0
                bullet2.neg = -1
                bullet2.count = 0
                bullet2.change = True
                bullet2.shoot = False
                bullet2.pressed = False
        self.stay_dead = False











    def death(self):

        if maps[mapnum][3][3] == True and self.stay_dead == False:
            self.spawn()
        else:
            for i in range(1000):
                self.particles.append(PARTICLES(self.x,self.y))
            if self.scoredead == False and self.nochanges == True:
                if self.playernum == 1:
                    player2.scoredead = True
                    player1.scoredead = False
                    player1.nochanges = False
                    player2.nochanges = False

                elif self.playernum == 2 and self.nochanges == True:
                    player1.scoredead = True
                    player2.scoredead = False
                    player1.nochanges = False
                    player2.nochanges = False




            self.dead_only_once = True


    def draw(self):
        global p1_color
        global p2_color
        if self.dead == False:
            if self.playernum == 1:

                if self.y<20:
                    pygame.draw.polygon(wn,p1_color,((self.x,10),(self.x-5,30),(self.x+5,30)),3)
                if self.mass == self.massmore:
                    pygame.draw.circle(wn,(255,255,255),(self.x,self.y),self.radius+2)

                pygame.draw.circle(wn,p1_color,(self.x,self.y),self.radius)

            if self.playernum == 2:
                if self.y<20:
                    pygame.draw.polygon(wn,p2_color,((self.x,10),(self.x-5,30),(self.x+5,30)),3)
                if self.mass == self.massmore:
                    pygame.draw.circle(wn,(255,255,255),(self.x,self.y),self.radius+2)

                pygame.draw.circle(wn,p2_color,(self.x,self.y),self.radius)
        else:
            for p in self.particles:
                p.draw()
            try:
                self.particles[0].check()
            except:
                pass

    def gravpull(self):
        self.y+=int(self.gravspeed)
        self.gravspeed+=self.originalgravspeed


    def checkdead(self):

        if self.dead == True and self.dead_only_once == False:
            self.death()
    def ways_to_die(self):
        if self.y>=700:
            self.dead = True


    def check(self,platform):

        aspeed = abs(self.speed)





        if self.x<=platform.platform[2]+platform.platform[0]+self.radius and self.x>=platform.platform[0]-self.radius:
            if self.y>platform.platform[1] and self.y<platform.platform[3]+platform.platform[1]:
                self.speed*=-1*platform.bouncy
                if platform.color == (0,0,0):
                    self.dead = True
                #left side
                if self.x>platform.platform[0]-self.radius and self.x<=platform.platform[0]+aspeed:
                    self.x = platform.platform[0]-self.radius
                    if platform.color == (0,0,0):
                        self.dead = True
                    #right side
                if self.x<platform.platform[0]+platform.platform[2]+self.radius and self.x>=platform.platform[0]+platform.platform[2]-aspeed:

                    self.x = platform.platform[0]+platform.platform[2]+self.radius
                    if platform.color == (0,0,0):
                        self.dead = True
        if self.y>=platform.platform[1]-self.radius and self.y<=platform.platform[1]+platform.platform[3]+self.radius and self.x>=platform.platform[0] and self.x<=platform.platform[2]+platform.platform[0]:
            if self.y<=platform.platform[3]+platform.platform[1]+self.radius and self.y>=platform.platform[1]+self.gravspeed+self.radius:
                self.y = platform.platform[3]+platform.platform[1]+self.radius+1
                if platform.color == (0,0,0):
                    self.dead = True
            elif self.y>=platform.platform[1]-self.radius and self.y<=platform.platform[1]+self.gravspeed+self.radius:

                self.y = platform.platform[1]-self.radius
                self.landed = True
                self.holdit = self.originalholdit
                if platform.color == (0,0,0):
                    self.dead = True
            self.gravspeed *= -1*platform.bouncy












    def move(self):
        if self.dead == False:
            keys = pygame.key.get_pressed()


            if self.playernum == 1:
                if keys[pygame.K_a]:
                    if bullet1.pressed == True:
                        bullet1.aimx+=bullet1.aimspeed * bullet1.neg
                    elif self.speed>=-1*self.maxspeed:
                        self.speed-=self.deltaspeed

                if keys[pygame.K_d]:
                    if bullet1.pressed == True:
                        bullet1.aimx-=bullet1.aimspeed * bullet1.neg
                    elif self.speed<=self.maxspeed:
                        self.speed+=self.deltaspeed
                if keys[pygame.K_w]:
                    if self.landed == True:
                        self.gravspeed+=self.holdit
                        self.holdit = self.holdit*0.8
                        if self.gravspeed>0:
                            self.landed = False
                if keys[pygame.K_s]:
                    self.gravspeed+=0.3

                if keys[pygame.K_q]:
                    self.mass = self.massmore
                if not keys[pygame.K_q]:
                    self.mass = self.massless
                if keys[pygame.K_ESCAPE]:
                    if bullet1.shoot == False:
                        bullet1.pressed = True
                if not keys[pygame.K_ESCAPE]:

                    if bullet1.pressed == True:
                        bullet1.shoot = True
                    bullet1.pressed = False



            if self.playernum == 2:
                if keys[pygame.K_LEFT]:
                    if bullet2.pressed == True:
                        bullet2.aimx+=bullet2.aimspeed * bullet2.neg
                    elif self.speed>=-1*self.maxspeed:
                        self.speed-=self.deltaspeed

                if keys[pygame.K_RIGHT]:
                    if bullet2.pressed == True:
                        bullet2.aimx-=bullet2.aimspeed * bullet2.neg
                    elif self.speed<=self.maxspeed:
                        self.speed+=self.deltaspeed

                if keys[pygame.K_UP]:
                    if self.landed == True:
                        self.gravspeed+=self.holdit
                        self.holdit = self.holdit*0.8
                        if self.gravspeed>0:
                            self.landed = False
                if keys[pygame.K_DOWN]:
                    self.gravspeed+=0.3

                if keys[pygame.K_SPACE]:
                    self.mass = self.massmore
                if not keys[pygame.K_SPACE]:
                    self.mass = self.massless
                if keys[pygame.K_m]:
                    if bullet2.shoot == False:
                        bullet2.pressed = True
                if not keys[pygame.K_m ]:

                    if bullet2.pressed == True:
                        bullet2.shoot = True
                    bullet2.pressed = False





            self.gravpull()
            for i in maps[mapnum][0]:
                self.check(i)
            bullet2.draw()
            bullet1.draw()
            self.x+=int(self.speed)
        #see if you died

        self.ways_to_die()
        self.checkdead()
class Bullet(object):
    def __init__(self,num):
        self.num = num

        if self.num == 1:
            self.x = player1.x
            self.y = player1.y
        if self.num == 2:
            self.x = player2.x
            self.y = player2.y

        self.dead = False
        self.shoot = False
        self.pressed = False

        self.aimlength = 50
        self.aimx = 0
        self.aimy = math.sqrt(100-(self.aimx)**2) + player2.y
        self.aimspeed = 2
        self.neg = -1

        self.radius = 10
        self.mass = 3
        self.aimy = math.sqrt(abs(100-self.aimx**2))

        self.rate = 3
        #x value related
        self.speed = 0

        #y value related
        self.change = True
        self.gravspeed = 0.4
        self.count = 0
        self.maxcount = 300
        self.originalgravspeed = self.gravspeed
    def checkdead(self):

        if self.count == self.maxcount:
            self.change = True
            self.shoot = False
            self.count = 0


    def gravpull(self):
        self.y+=int(self.gravspeed)//self.rate
        self.gravspeed+=self.originalgravspeed

    def check(self,platform):
        aspeed = abs(self.speed)





        if self.x<=platform.platform[2]+platform.platform[0]+self.radius and self.x>=platform.platform[0]-self.radius:
            if self.y>platform.platform[1] and self.y<platform.platform[3]+platform.platform[1]:
                self.speed*=-1*platform.bouncy

                #left side
                if self.x>platform.platform[0]-self.radius and self.x<=platform.platform[0]+aspeed:
                    self.x = platform.platform[0]-self.radius

                    #right side
                if self.x<platform.platform[0]+platform.platform[2]+self.radius and self.x>=platform.platform[0]+platform.platform[2]-aspeed:

                    self.x = platform.platform[0]+platform.platform[2]+self.radius

        if self.y>=platform.platform[1]-self.radius and self.y<=platform.platform[1]+platform.platform[3]+self.radius and self.x>=platform.platform[0] and self.x<=platform.platform[2]+platform.platform[0]:
            if self.y<=platform.platform[3]+platform.platform[1]+self.radius and self.y>=platform.platform[1]+self.gravspeed+self.radius:
                self.y = platform.platform[3]+platform.platform[1]+self.radius+1

            elif self.y>=platform.platform[1]-self.radius and self.y<=platform.platform[1]+self.gravspeed+self.radius:

                self.y = platform.platform[1]-self.radius


            self.gravspeed *= -1*platform.bouncy




    def draw(self):
        if self.shoot == False:
            if self.num == 2 and player2.dead==False:
                #pygame.draw.circle(wn,(100,50,200),(self.x,self.y),self.radius)
                self.x = player2.x
                self.y = player2.y
            if self.num == 1 and player1.dead==False:
                #pygame.draw.circle(wn,(100,200,50),(self.x,self.y),self.radius)
                self.x = player1.x
                self.y = player1.y


        if self.pressed == True:
            if self.num == 2 and player2.dead == False:
                pygame.draw.line(wn,(255,255,255),(player2.x,player2.y),(self.aimx+player2.x,self.aimy+player2.y))
            if self.num == 1 and player1.dead == False:
                pygame.draw.line(wn,(255,255,255),(player1.x,player1.y),(self.aimx+player1.x,self.aimy+player1.y))
        #(x)**2 + (y)**2 = radius
        # = sqrt(radius-(x-a)**2)

        if self.aimx>self.aimlength:
            self.aimx = self.aimlength
            self.neg *= -1

        if self.aimx<-1*self.aimlength:
            self.aimx = -1*self.aimlength
            self.neg *= -1

        self.aimy = math.sqrt(self.aimlength**2-(self.aimx)**2)*self.neg


        if self.shoot == True:
            self.count+=1
            if self.change == True:
                self.gravspeed = (self.aimy)
                self.speed = (self.aimx)
                self.change = False
            if self.num == 2 and player2.dead!=True:
                pygame.draw.circle(wn,p2_color,(self.x,self.y),self.radius)
            if self.num == 1 and player1.dead!=True:
                pygame.draw.circle(wn,p1_color,(self.x,self.y),self.radius)

            self.gravpull()
            for i in maps[mapnum][0]:
                self.check(i)
            self.x+=int(self.speed)//self.rate
            self.checkdead()






class CAPTURE(object):
    def __init__(self,x,y,radius,rate):
        self.radius = radius
        self.fillinradius = 0
        self.x = x
        self.y = y
        self.stop = False
        self.rate = rate
    def isitin(self,t2):
        if t2.dead == False:
            distance = math.sqrt(math.pow(self.x-t2.x,2)+math.pow(self.y-t2.y,2))
            if distance <= self.radius+t2.radius:
                return True
            else:
                return False
        else:
            return False
    def draw(self):
        if self.fillinradius >= int((self.radius-2)*(1/self.rate)):
            pygame.draw.circle(wn,(255,0,0),(self.x,self.y),self.radius,2)
            player2.dead = True
            player2.stay_dead = True
            self.stop = True
        elif self.fillinradius <= int(((self.radius-2)*-1)*(1/self.rate)):
            pygame.draw.circle(wn,(255,0,0),(self.x,self.y),self.radius,2)
            player1.dead = True
            player1.stay_dead = True
            self.stop = True
        else:
            pygame.draw.circle(wn,(255,255,255),(self.x,self.y),self.radius,2)

        if self.fillinradius !=0:
            if self.fillinradius>0:
                pygame.draw.circle(wn,(abs(p1_color[0]-40),abs(p1_color[1]-40),abs(p1_color[2]-40)),(self.x,self.y),int(abs(self.fillinradius)*self.rate))
            if self.fillinradius<0:
                pygame.draw.circle(wn,(abs(p2_color[0]-40),abs(p2_color[1]-40),abs(p2_color[2]-40)),(self.x,self.y),int(abs(self.fillinradius)*self.rate))

        if self.isitin(player1) and self.stop == False:
            self.fillinradius +=1

        if self.isitin(player2) and self.stop == False:
            self.fillinradius -=1















maps = []


map1 = [[PLATFORM(550,400,100,100,(255,255,255),0.4,0,0,0,[None,None]),
         PLATFORM(0,600,1200,50,(255,255,255),0.5,0,0,0,[None,None]),
         PLATFORM(50,100,100,100,(100,200,50),0.8,5,0,0,[1050,None]),
         PLATFORM(1050,100,100,100,(100,50,200),0.8,-5,0,0,[50,None]),
         PLATFORM(550,100,100,100,(0,0,0),0.8,0,0,0,[None,None]),
         PLATFORM(1190,500,50,100,(255,255,255),0.8,0,0,0,[None,None]),
         PLATFORM(-40,500,50,100,(255,255,255),0.8,0,0,0,[None,None])],
        [CAPTURE(600,300,600,17)],
        [100,50],
        [1100,50,True,False]]


map2 = [[PLATFORM(500,10,100,590,(0,0,0),0,1,0,0,[600,None]),
         PLATFORM(0,600,100,50,(75,75,75),0.5,0,0,0,[None,None]),
         PLATFORM(150,600,100,50,(75,75,75),0.5,0,0,0,[None,None]),
         PLATFORM(300,600,100,50,(75,75,75),0.5,0,0,0,[None,None]),
         PLATFORM(450,600,150,50,(75,75,75),0.5,0,0,0,[None,None]),
         PLATFORM(600,600,150,50,(75,75,75),0.5,0,0,0,[None,None]),
         PLATFORM(800,600,100,50,(75,75,75),0.5,0,0,0,[None,None]),
         PLATFORM(950,600,100,50,(75,75,75),0.5,0,0,0,[None,None]),
         PLATFORM(1100,600,100,50,(75,75,75),0.5,0,0,0,[None,None])],
        [CAPTURE(600,300,100,1)],
        [50,50],
        [1150,50,True,False]]


map3 = [[PLATFORM(0,10,100,245,(0,0,0),0,5,7,0,[1100,355]),
         PLATFORM(1100,10,100,245,(0,0,0),0,-5,7,0,[0,355]),
         PLATFORM(0,600,1200,50,(255,255,255),0.75,0,0,0,[None,None]),
         PLATFORM(1190,0,10,600,(255,255,255),0.75,0,0,0,[None,None]),
         PLATFORM(0,0,10,600,(255,255,255),0.75,0,0,0,[None,None]),
         PLATFORM(0,0,1200,10,(255,255,255),0.75,0,0,0,[None,None])],
        [],
        [100,500],
        [1050,500,True, False]]
ran = 20
map4 = [[PLATFORM(0,600,1200,50,(255,255,255),0.75,0,1,0,[None,600+(650+100*(ran-1))//3]),
         PLATFORM(0,0,1200,10,(255,255,255),0.75,0,0,0,[None,None]),
         PLATFORM(0,0,10,600,(0,0,0),0.75,0,0,0,[None,None]),
         PLATFORM(1190,0,10,600,(0,0,0),0.75,0,0,0,[None,None])
         ],
        [],
        [700,500],
        [700,500,False, False]]

for x in range(ran):
    a = int(random.randint(50,350))
    b = (int(x)*200+1200)
    c = (int(ran)*200+1200)
    map4[0].append(PLATFORM(b,0,100,a,(0,255,0),0.75,-3,0,0,[b-c+100,None]))
    map4[0].append(PLATFORM(b,a+100,100,700-a,(0,255,0),0.75,-3,0,0,[b-c+100,None]))
map5rate = 10
map5 = [[PLATFORM(0,0,10,700,(255,255,255),0.75,0,0,0,[None,None]),
         PLATFORM(1190,0,10,700,(255,255,255),0.75,0,0,0,[None,None]),
         PLATFORM(0,650,1200,50,(255,255,255),0.9,0,0,0,[None,None]),
         PLATFORM(1200,650,100,50,(255,255,255),0.9,0,0,0,[None,None]),
         PLATFORM(1310,-1000,10,1700,(255,255,255),0,0,0,0,[None,None]),
         PLATFORM(10,50,50,10,(255,255,255),0,map5rate,0,0,[1140,None]),
         PLATFORM(10,75,50,10,(0,0,0),0,20,0,0,[1140,None]),
         PLATFORM(10,275,50,10,(0,0,0),0,20,0,0,[1140,None]),
         PLATFORM(10,150,50,10,(255,255,255),0,map5rate,0,0,[1140,None]),
         PLATFORM(10,250,50,10,(255,255,255),0,map5rate,0,0,[1140,None]),
         PLATFORM(10,350,50,10,(255,255,255),0,map5rate,0,0,[1140,None]),
         PLATFORM(10,450,50,10,(255,255,255),0,map5rate,0,0,[1140,None]),
         PLATFORM(10,550,50,10,(255,255,255),0,map5rate,0,0,[1140,None]),
         PLATFORM(1140,0,50,10,(255,255,255),0,-map5rate,0,0,[10,None]),
         PLATFORM(1140,100,50,10,(255,255,255),0,-map5rate,0,0,[10,None]),
         PLATFORM(1140,200,50,10,(255,255,255),0,-map5rate,0,0,[10,None]),
         PLATFORM(1140,300,50,10,(255,255,255),0,-map5rate,0,0,[10,None]),
         PLATFORM(1140,400,50,10,(255,255,255),0,-map5rate,0,0,[10,None]),
         PLATFORM(1140,500,50,10,(255,255,255),0,-map5rate,0,0,[10,None])

         ],
        [CAPTURE(1250,600,50,10),
         CAPTURE(600,0,50,0.1)],
        [700,500],
        [600,500,True,False]]

map6 = [[PLATFORM(0,690,1200,10,(255,255,255),0,0,0,0,[None, None]),
         PLATFORM(0,0,1200,10,(255,255,255),0,0,0,0,[None, None]),
         PLATFORM(1100,680,100,20,(255,255,255),1,0,0,0,[None, None]),
         PLATFORM(0,505,100,20,(255,255,255),1,0,0,0,[None, None]),
         PLATFORM(1100,330,100,20,(255,255,255),1,0,0,0,[None, None]),
         PLATFORM(-100,515,1200,10,(255,255,255),0,0,0,0,[None, None]),
         PLATFORM(100,340,1200,10,(255,255,255),0,0,0,0,[None, None]),
         PLATFORM(-100,165,1200,10,(255,255,255),0,0,0,0,[None, None]),
         PLATFORM(0,0,10,700,(255,255,255),1,0,0,0,[None,None]),
         PLATFORM(1190,0,10,700,(255,255,255),1,0,0,0,[None,None]),

         PLATFORM(150,600,100,105,(0,0,0),1,0,0,0,[None,None]),
         PLATFORM(400,600,100,105,(0,0,0),1,0,0,0,[None,None]),
         PLATFORM(700,350,10,50,(0,0,0),1,0,12,0,[None,640]),
         PLATFORM(750,350,10,50,(0,0,0),1,0,9,0,[None,640]),
         PLATFORM(800,350,10,50,(0,0,0),1,0,7,0,[None,640]),
         PLATFORM(850,350,10,50,(0,0,0),1,0,5,0,[None,640]),
         PLATFORM(200,350,20,20,(0,0,0),1,10,5,0,[500,465]),
         PLATFORM(200,350,20,20,(0,0,0),1,5,10,0,[500,465]),],
        [CAPTURE(0,75,75,50)],
        [50,650],
        [50,650,False,True]]



maps.append(map1)
maps.append(map2)
maps.append(map3)
maps.append(map4)
maps.append(map5)
maps.append(map6)










mapnum = 0

player1 = PLAYER(1,20)
player2 = PLAYER(2,20)
bullet1 = Bullet(1)
bullet2 = Bullet(2)



























def collide(t1,t2):
    #elastic collision
    #mass * velocity^2 = KE
    #P = mass * velocity
    #P_initial = P_final
    #P_p1_initial + P_p2_initial = P_p1_final + P_p2_final

    if t1.dead == False and t2.dead == False:
        twice = 1
        distance = math.sqrt(math.pow(t1.x-t2.x,2)+math.pow(t1.y-t2.y,2))

        if distance <= t1.radius+t2.radius:
            if distance<t1.radius+t2.radius-2:
                twice = 1.2
                if t1.y>t2.y:
                    t1.y+=4
                    t2.y-=4
                if t1.y<t2.y:
                    t1.y-=4
                    t2.y+=4

            ratio = t2.mass/t1.mass
            k1 = (1-ratio) / (1+ratio)
            k2 = 2 / (1+ratio)

            #x calculation

            speed1_f = k1 * t1.speed + k2 * ratio * t2.speed * twice
            speed2_f = k2 * t1.speed - k1 * t2.speed * twice


            t1.speed = speed1_f
            t2.speed = speed2_f
            #y calculation
            speed1_f = k1 * t1.gravspeed + k2 * ratio * t2.gravspeed * twice
            speed2_f = k2 * t1.gravspeed - k1 * t2.gravspeed * twice

            t1.gravspeed = speed1_f
            t2.gravspeed = speed2_f






def draw():

    refill()
    player2.write()
    player1.write()
    if maps[mapnum][3][2] == True:
        collide(player1,player2)
        collide(player1,bullet2)
        collide(bullet1,player2)
        collide(bullet1,bullet2)
    for cap1 in maps[mapnum][1]:
        cap1.draw()

    player2.draw()

    player1.draw()


    for i in maps[mapnum][0]:
        i.draw()

    if stop == False:
        refill2()
        pygame.display.update()








run = True
stop = True
while run:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = False
    if stop == False:
        xval-=24
        yval-=14
    if xval<=0:
        run = False
    draw()
    player1.move()
    player2.move()

    pygame.display.update()
    wn = pygame.display.set_mode((xval,yval))
pygame.quit()
