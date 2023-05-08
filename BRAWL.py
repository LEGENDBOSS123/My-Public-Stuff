import pygame
pygame.init()
import random
import math
import socket
import time
fps = 60

xval = 2000
yval = 1000
IP = input("IP: ")

port = 4000
wn = pygame.display.set_mode((xval,yval))
def ENCODE(lis):
    ret = ""
    for i in lis:
        ret2 = ""
        for o in i:
            ret2+=","+str(o)+","
        ret+=" "+ret2+" "
    return ret
def DECODE(string):
    ret = string.split()
    for i in range(len(ret)):
        ret[i] = ret[i].split(',')
        
        
        
            
                
        while '' in ret[i]:
            ret[i].remove("")

        for a in range(len(ret[i])):
            if ret[i][a][0]=="-":
                if ret[i][a][1:].isdigit():
                    ret[i][a] = int(ret[i][a])
            elif ret[i][a].isdigit():
                    ret[i][a] = int(ret[i][a])
    return ret
def project_verticies(axis,v,a):
    mini = 99999999999999999999
    maxi = -99999999999999999999

    for i in range(len(v)):
        Vec = v[i]
        projection = Vec[0]*axis[0]+Vec[1]*axis[1]
        if projection<mini:
            mini = projection
        if projection>maxi:
            maxi = projection
    
    return (mini,maxi)
def project_circle_verticies(axis,b):
    direction = (axis[0]*b[2],axis[1]*b[2])
    p1 = (b[0]+direction[0],b[1]+direction[1])
    p2 = (b[0]-direction[0],b[1]-direction[1])
    
    mini = p1[0]*axis[0]+p1[1]*axis[1]
    maxi = p2[0]*axis[0]+p2[1]*axis[1]

    if mini>maxi:
        e = mini
        z = maxi
        mini = z
        maxi = e
    return (mini,maxi)
def closest_point_on_polygon(a,b):
    sx = a[0]
    sy = a[1]
    sw = a[2]
    sh = a[3]
    sv = [(sx,sy),(sx+sw,sy),(sx+sw,sy+sh),(sx,sy+sh)]
    cx = b[0]
    cy = b[1]
    cr = b[2]
    ac = (sx+sw/2,sy+sh/2)
    result = 0
    mini = 99999999999999999999
    for i in range(len(sv)):
        v = (sv[i][0],sv[i][1])
        dis = math.sqrt((v[0]-b[0])**2+(v[1]-b[1])**2)

        if dis<mini:
            mini = dis
            result = i
            
    return result


    
def polygon_circle_intersect(a,b):
    depth = 99999999999999999999
    normal = 0
    axis = 0
    depthA = 0
    sx = a[0]
    sy = a[1]
    sw = a[2]
    sh = a[3]
    sv = [(sx,sy),(sx+sw,sy),(sx+sw,sy+sh),(sx,sy+sh)]
    cx = b[0]
    cy = b[1]
    cr = b[2]
    ac = (sx+sw/2,sy+sh/2)
    
    for i in range(len(sv)):
        va = sv[i]
        vb = sv[(i+1)%len(sv)]

        edge = (vb[0]-va[0],vb[1]-va[1])
    
        axis = (-edge[1],edge[0])
        l = math.sqrt(axis[0]**2+axis[1]**2)
        if l==0:
            axis = (1,0)
        else:
            axis = (-edge[1]/l,edge[0]/l)
        
        first = project_verticies(axis, sv,a)
        
        second = project_circle_verticies(axis,b)
        
        if first[0] >= second[1] or first[1] <= second[0]:
            return False
        
        depthA = min(abs(second[1]-first[0]),abs(first[1]-second[0]))            
        if depthA<depth:
            depth = depthA
            normal = axis
    cpindex = closest_point_on_polygon(a,b)
    cp = (sv[cpindex][0],sv[cpindex][1])
    axis = (cp[0]-b[0],cp[1]-b[1])
    l = math.sqrt(axis[0]**2+axis[1]**2)
    if l==0:
        axis = (1,0)
    else:
        axis = (-edge[1]/l,edge[0]/l)
        
    first = project_verticies(axis,sv,a)
    second = project_circle_verticies(axis,b)
    
    if first[0] >= second[1] or first[1] <= second[0]:
        return False
    
    depthA = min(abs(second[1]-first[0]),abs(first[1]-second[0]))          
    if depthA<depth:
        depth = depthA
        normal = axis
        
    
    direction = (b[0]-ac[0],b[1]-ac[1])
    dp = direction[0]*normal[0]+direction[1]*normal[1]
    if dp<0:
        normal = (-normal[0],-normal[1])
    return (normal,depth)

class BUTTON():
    def __init__(self,Id,x,y,w,h,text,color,textcolor,function,args,visibility):
        self.ID = Id;
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.font = pygame.font.SysFont("Merriwheather bold",2*self.w//len(self.text))
        self.textcolor = textcolor
        self.drawntext = self.font.render(self.text,False,textcolor)
        
        self.color = color
        self.hover_color = [int(color[0]/1.1),int(color[1]/1.1),int(color[2]/1.1)]
        self.function = function
        self.args = args
        self.rect = [x,y,w,h]
        self.visible =  visibility

        
        
    def HOVERING(self):
        hovering = False
        pos = pygame.mouse.get_pos()
        xpos = pos[0]
        ypos = pos[1]
        if xpos > self.x and xpos < self.x+self.w and ypos > self.y and ypos < self.y+self.h:
            hovering = True
        return hovering
    
    def CLICK(self):
        if self.function!=None:
            if self.args==None:
                self.function()
            else:
                self.function(self.args)
    
    def DRAW(self):
        click = False
        if self.visible:
            if self.HOVERING():
                pygame.draw.rect(wn,self.hover_color,(self.x,self.y,self.w,self.h))
                if pygame.mouse.get_pressed()[0]:
                    self.CLICK()
                    click = True
            else:
                pygame.draw.rect(wn,self.color,(self.x,self.y,self.w,self.h))
            size = self.drawntext.get_size()
            wn.blit(self.drawntext,((2*self.x+self.w)//2-size[0]//2,(2*self.y+self.h)//2-size[1]//2))
        return click
            
    def HIDE(self):
        self.visible = False
        
    def SHOW(self):
        self.visible = True
    def TEXT(self,text):
        self.text = text
        self.font = pygame.font.SysFont("Merriwheather bold",2*self.w//len(self.text))
        self.drawntext = self.font.render(self.text,False,self.textcolor)


            
            
        
class BUTTON_MANAGER():
    def __init__(self):
        self.buttons = []
        
    def CREATE_BUTTON(self,Id,x,y,w,h,text,color,textcolor,function,args,visibility):
        self.buttons.append(BUTTON(Id,x,y,w,h,text,color,textcolor,function,args,visibility))
    def DRAW(self):
        for i in self.buttons:
            if i.DRAW():
                pygame.time.delay(100)
                return
                
    def FIND(self,ID):
        for i in self.buttons:
            if i.ID == ID:
                return i
            

class PLAYER():
    def __init__(self):
        self.angle = 0
        self.map = []
        self.ammo = 3
        self.x = 0
        self.y = 0
        self.speed = 7
        self.BRAWLER = "SHELLY"
        self.ALL_BRAWLERS = ["SHELLY","COLT","ROUNDY","DEFENDY","PIPER","BOWLER","JOE","TANKY","NUKER","FIRECRACKER","SATISFACTION","BANDIT","CLASHER"]
        self.ingame = 1
        self.gamemode = 2
        self.playersfound = [0,0]
        self.HP = 1000
        self.OGHP=self.HP
        self.buttons = BUTTON_MANAGER()
        self.buttons.CREATE_BUTTON("START",int(xval/1.2-20),int(yval/1.2-20),int(xval/6),int(yval/6),"PLAY",(247, 210, 0),(250,250,250),self.START,None,True)
        self.buttons.CREATE_BUTTON("BRAWLERS",int(20),int(yval/1.2-20),int(xval/6),int(yval/6),"BRAWLERS",(247, 210, 0),(250,250,250),self.BRAWLER_PAGE,None,True)
        self.buttons.CREATE_BUTTON("END",int(20),int(20),int(xval/10),int(yval/10),"END",(247, 210, 0),(250,250,250),self.END,None,False)
        self.buttons.CREATE_BUTTON("PLAYERS",int(9*xval/20),int(20),int(xval/10),int(yval/10),str(self.playersfound[0])+" / "+str(self.playersfound[1]),(247, 210, 0),(250,250,250),None,None,False)
        self.buttons.CREATE_BUTTON("GAMEMODE",int(5*xval/12),int(yval/1.2-20),int(xval/6),int(yval/6),"GAMEMODE: "+str(self.gamemode),(247, 210, 0),(250,250,250),self.GAMEMODE_PAGE,None,True)
        self.buttons.CREATE_BUTTON("CHOSEN_BRAWLER",int(xval/3),int(yval/3),int(xval/3),int(yval/3),self.BRAWLER,(247, 210, 0),(250,250,250),self.BRAWLER_PAGE,None,True)
        
        self.buttons.CREATE_BUTTON("EXIT_BRAWLER_PAGE",int(20),int(20),int(xval/10),int(yval/10),"EXIT",(247, 210, 0),(250,250,250),self.EXIT_BRAWLER_PAGE,None,False)
        self.buttons.CREATE_BUTTON("EXIT_GAMEMODE_PAGE",int(20),int(20),int(xval/10),int(yval/10),"EXIT",(247, 210, 0),(250,250,250),self.EXIT_GAMEMODE_PAGE,None,False)
        for i in range(len(self.ALL_BRAWLERS)):
            self.buttons.CREATE_BUTTON(self.ALL_BRAWLERS[i],int(3*((i+3)%3)/12*xval+xval/7.5),int(int(i/3)*1/6*yval+30*int(i/3)+30),int(xval/6),int(yval/6),self.ALL_BRAWLERS[i],(247, 210, 0),(250,250,250),self.CHOSEN_BRAWLER,[self.ALL_BRAWLERS[i]],False)
        for i in range(4):
            self.buttons.CREATE_BUTTON(str(i+2),int(3*((i+3)%3)/12*xval+xval/7.5),int(int(i/3)*1/6*yval+30*int(i/3)+30),int(xval/6),int(yval/6),str(i+2)+" PLAYERS",(247, 210, 0),(250,250,250),self.GAMEMODE,[i],False)

        self.bullets = []
        self.hit = []
        self.radius = 30
        self.visible = 1
        self.ammo = 300
        self.reload = 30
        self.visible_counter = 100

    def GAME_START(self):
        if self.BRAWLER == "SHELLY":
            self.OGHP = 1000
        elif self.BRAWLER == "COLT":
            self.OGHP = 750
        elif self.BRAWLER == "ROUNDY":
            self.OGHP = 1000
        elif self.BRAWLER == "DEFENDY":
            self.OGHP = 2000
        elif self.BRAWLER == "BANDIT":
            self.OGHP = 825
        elif self.BRAWLER == "PIPER":
            self.OGHP = 500
        elif self.BRAWLER == "BOWLER":
            self.OGHP = 1250
        elif self.BRAWLER == "JOE":
            self.OGHP = 950
        elif self.BRAWLER == "TANKY":
            self.OGHP = 5000
        elif self.BRAWLER == "NUKER":
            self.OGHP = 500
        elif self.BRAWLER == "FIRECRACKER":
            self.OGHP = 1000
        elif self.BRAWLER == "SATISFACTION":
            self.OGHP = 1000
        elif self.BRAWLER == "CLASHER":
            self.OGHP = 900
        
        
        self.HP = self.OGHP
        self.bullets = []
        self.hit = []
        self.ammo = 300
        
        
    def START(self):
        self.GAME_START()
        self.ingame = 2
        for i in self.buttons.buttons:
            i.HIDE()
        self.buttons.FIND("END").SHOW()
        self.buttons.FIND("PLAYERS").SHOW()

    def END(self):
        self.ingame = 1
        self.HP = self.OGHP
        self.bullets = []
        self.hit = []
        self.ammo = 300
        self.ingame = 1
        self.buttons.FIND("CHOSEN_BRAWLER").SHOW()
        self.buttons.FIND("START").SHOW()
        self.buttons.FIND("BRAWLERS").SHOW()
        self.buttons.FIND("GAMEMODE").SHOW()
        self.buttons.FIND("END").HIDE()
        self.buttons.FIND("PLAYERS").HIDE()
    
    def BRAWLER_PAGE(self):
        for i in self.buttons.buttons:
            i.HIDE()
        for i in self.ALL_BRAWLERS:
            if i!=self.BRAWLER:
                self.buttons.FIND(i).SHOW()
        self.buttons.FIND("EXIT_BRAWLER_PAGE").SHOW()

    def EXIT_BRAWLER_PAGE(self):
        self.buttons.FIND("EXIT_BRAWLER_PAGE").HIDE()
        for i in self.ALL_BRAWLERS:
            self.buttons.FIND(i).HIDE()
        
            
        self.buttons.FIND("CHOSEN_BRAWLER").SHOW()
        self.buttons.FIND("CHOSEN_BRAWLER").TEXT(self.BRAWLER)

        self.buttons.FIND("START").SHOW()
        self.buttons.FIND("BRAWLERS").SHOW()
        self.buttons.FIND("GAMEMODE").SHOW()
    def CHOSEN_BRAWLER(self,args):

        self.BRAWLER = args[0]
        self.EXIT_BRAWLER_PAGE()
    def GAMEMODE_PAGE(self):
        for i in self.buttons.buttons:
            i.HIDE()
        for i in range(4):
            self.buttons.FIND(str(i+2)).SHOW()
        self.buttons.FIND("EXIT_GAMEMODE_PAGE").SHOW()
    def EXIT_GAMEMODE_PAGE(self):
        self.buttons.FIND("EXIT_GAMEMODE_PAGE").HIDE()
        for i in range(4):
            self.buttons.FIND(str(i+2)).HIDE()
        self.buttons.FIND("CHOSEN_BRAWLER").SHOW()
        self.buttons.FIND("CHOSEN_BRAWLER").TEXT(self.BRAWLER)

        self.buttons.FIND("START").SHOW()
        self.buttons.FIND("BRAWLERS").SHOW()
        self.buttons.FIND("GAMEMODE").SHOW()
    def GAMEMODE(self,args):
        self.gamemode = args[0]+2
        self.EXIT_GAMEMODE_PAGE()
    def SHOOT(self):
        self.ammo+=1
        if self.reload<30:
            self.reload-=1
        if self.reload<0:
            self.reload = 30
        if self.ammo>300:
            self.ammo = 300
        if self.ammo<0:
            self.ammo = 0
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        angle = 0
        if xval//2-mouse[0] != 0:
            angle = 180/math.pi*math.atan((yval//2-mouse[1])/(xval//2-mouse[0]))
        if mouse[0]-xval//2<=0:
            angle+=180
        if (keys[pygame.K_SPACE] or keys[pygame.K_q]) and self.reload == 30:
            if self.ammo>=100:
                self.visible_counter = 99
                self.ammo-=100
                self.reload-=1
                if self.BRAWLER == "ROUNDY":
                    for i in range(30):
                        self.bullets.append([self.x,self.y,200,math.cos((angle+i*12)*math.pi/180)*15,math.sin((angle+i*12)*math.pi/180)*15,0,400,5])
                if self.BRAWLER == "SHELLY":
                    for i in range(11):
                        self.bullets.append([self.x,self.y,100,math.cos((angle-25+i*5)*math.pi/180)*15,math.sin((angle-25+i*5)*math.pi/180)*15,0,350,5])
                if self.BRAWLER == "COLT":
                    for i in range(15):
                        self.bullets.append([self.x,self.y,50,math.cos((angle)*math.pi/180)*(i+5),math.sin((angle)*math.pi/180)*(i+5),0,650,5])
                if self.BRAWLER == "DEFENDY":
                    for i in range(20):
                        self.bullets.append([self.x,self.y,25,math.cos((angle+i*18)*math.pi/180)*3,math.sin((angle+i*18)*math.pi/180)*3,0,100,5])
                    for i in range(3):
                        self.bullets.append([self.x,self.y,100,math.cos((angle)*math.pi/180)*(i+5),math.sin((angle)*math.pi/180)*(i+5),0,350,5])
                if self.BRAWLER == "BANDIT":
                    self.x+=math.cos((angle)*math.pi/180)*200
                    self.y+=math.sin((angle)*math.pi/180)*200
                    self.bullets.append([self.x,self.y,250,math.cos((angle)*math.pi/180)*5,math.sin((angle)*math.pi/180)*5,0,1,50])
                    
                if self.BRAWLER == "PIPER":
                    self.bullets.append([self.x,self.y,50,math.cos((angle)*math.pi/180)*15,math.sin((angle)*math.pi/180)*15,0,750,5])
                if self.BRAWLER == "BOWLER":
                    self.bullets.append([self.x,self.y,350,math.cos((angle)*math.pi/180)*10,math.sin((angle)*math.pi/180)*10,0,500,50])
                if self.BRAWLER == "JOE":
                    for i in range(23):
                        self.bullets.append([self.x,self.y,25,math.cos((angle+i*2-22)*math.pi/180)*(abs(22-2*i)+3),math.sin((angle+i*2-22)*math.pi/180)*(abs(22-2*i)+3),0,500,10])    
                if self.BRAWLER == "TANKY":
                    for i in range(3):
                        self.bullets.append([self.x,self.y,30,math.cos((angle+10*i-10)*math.pi/180)*10,math.sin((angle+10*i-10)*math.pi/180)*10,0,350,10])
                if self.BRAWLER == "NUKER":
                    self.bullets.append([self.x,self.y,100000,0,0,0,300,30])
                    
                if self.BRAWLER == "FIRECRACKER":
                    self.bullets.append([self.x,self.y,250,math.cos((angle)*math.pi/180)*15,math.sin((angle)*math.pi/180)*15,0,450,20])
                if self.BRAWLER == "SATISFACTION":
                    self.reload = 30
                    self.ammo = 300
                    self.bullets.append([mouse[0]+self.x-xval/2,mouse[1]+self.y-yval/2,10,0,0,0,100,20])
                if self.BRAWLER == "CLASHER":
                    
                    for i in range(5,15,5):
                        self.bullets.append([self.x,self.y,100,math.cos((angle)*math.pi/180)*i,math.sin((angle)*math.pi/180)*i,0,500,5])
                        for e in range(0,30,10):
                            
                            self.bullets.append([self.x,self.y,100,math.cos((angle+e)*math.pi/180)*i,math.sin((angle+e)*math.pi/180)*i,0,500,5])
                            self.bullets.append([self.x,self.y,100,math.cos((angle-e)*math.pi/180)*i,math.sin((angle-e)*math.pi/180)*i,0,500,5])
        
    def GAME(self,p):
        won = False
        self.buttons.FIND("PLAYERS").HIDE()
        self.buttons.FIND("END").HIDE()
        if self.HP>self.OGHP:
            self.HP = self.OGHP
        if self.HP<=0:
            self.buttons.FIND("END").CLICK()
        vis = 1
        for b in self.bullets[:]:
            b[0]+=b[3]
            b[1]+=b[4]
            b[5]+=math.sqrt(b[3]**2+b[4]**2)
            if self.BRAWLER=="PIPER":
                b[7] = b[5]/b[6]*20
                b[2] = b[5]/b[6]*500+50
            
            if b[5]>=b[6]:
                if self.BRAWLER == "FIRECRACKER" and b[7]==20:
                    self.bullets.append([b[0],b[1],150,0,7,0,200,10])
                    self.bullets.append([b[0],b[1],150,7,0,0,200,10])
                    self.bullets.append([b[0],b[1],150,0,-7,0,200,10])
                    self.bullets.append([b[0],b[1],150,-7,0,0,200,10])
                    self.bullets.append([b[0],b[1],150,5,5,0,200,10])
                    self.bullets.append([b[0],b[1],150,5,-5,0,200,10])
                    self.bullets.append([b[0],b[1],150,-5,5,0,200,10])
                    self.bullets.append([b[0],b[1],150,-5,-5,0,200,10])
                self.bullets.remove(b)
                
        for i in range(len(self.maps)):
            if self.maps[i] == "W":
                c = polygon_circle_intersect([i%20*100,int(i/20)*100,100,100],[self.x,self.y,self.radius])
                if c!=False:

                    normal = c[0]
                    depth = c[1]+1

                    dc = (normal[0]*depth,normal[1]*depth)
                    self.x += dc[0]
                    self.y += dc[1]
            
            if self.maps[i] == "B":
                
                c = polygon_circle_intersect([i%20*100,int(i/20)*100,100,100],[self.x,self.y,self.radius])
                if c!=False:
                    vis = 0
                    
        for b in self.bullets[:]:
            for i in range(len(self.maps)):
                if self.maps[i] == "W":
                    c = polygon_circle_intersect([i%20*100,int(i/20)*100,100,100],[b[0],b[1],b[7]])
                    if c!=False:
                        if b in self.bullets:
                            self.bullets.remove(b)
                
                
            
        self.visible = vis
        for i in range(len(self.maps)):
            if self.maps[i] == "W":
                pygame.draw.rect(wn,(222,184,135),(i%20*100-self.x+xval//2,int(i/20)*100-self.y+yval//2,100,100))
                
            if self.maps[i] == "G" or type(self.maps[i])==int:
                pygame.draw.rect(wn,(255,200,150),(i%20*100-self.x+xval//2,int(i/20)*100-self.y+yval//2,100,100))
            if self.maps[i] == "B":
                
                pygame.draw.rect(wn,(0,150,0),(i%20*100-self.x+xval//2,int(i/20)*100-self.y+yval//2,100,100))
                
                
            
        
           
            
        self.SHOOT()
        if self.visible_counter !=100:
            self.visible_counter-=1
            self.visible = 1
        
        if self.visible_counter <= 0:
            self.visible_counter = 100
        
        for i in p:
            if i[0] == "WON":
                won = True
            if i[0]=="HIT":
                self.HP-=i[2]
                self.visible_counter = 99
            if i[0]=="PLAYER":
                if i[6]==1 or math.sqrt((i[1]-self.x)**2+(i[2]-self.y)**2)<125:
                    pygame.draw.circle(wn,(255,30,30),(int(i[1]-self.x+xval//2),int(i[2]-self.y+yval//2)),self.radius)
                    pygame.draw.rect(wn,(0,0,0),(int(i[1]-self.x+xval//2-50),int(i[2]-self.y+yval//2-75),100,20))
                    pygame.draw.rect(wn,(255,100,100),(int(i[1]-self.x+xval//2-50),int(i[2]-self.y+yval//2-75),int(100*i[4]/i[5]),20))
                    font = pygame.font.SysFont("Merriwheather bold",2*55//len(i[3]))
                    drawntext = font.render(i[3],False,(200,200,200))
                    size = drawntext.get_size()
                    wn.blit(drawntext,(int(i[1]-self.x+xval//2-size[0]/2),int(i[2]-self.y+yval//2-size[1]/2)))
                for e in self.bullets[:]:
                    if math.sqrt((i[1]-e[0])**2+(i[2]-e[1])**2)<=self.radius+e[7]:
                        if self.BRAWLER == "BANDIT":
                            self.ammo+=100
                        
                        self.hit.append([i[7],e[2]])
                        
                        self.bullets.remove(e)
                        
                        
            if i[0]=="BULLET":
                pygame.draw.circle(wn,(255,30,30),(int(i[1]-self.x+xval//2),int(i[2]-self.y+yval//2)),i[3])

        pygame.draw.circle(wn,(30,30,255),(xval//2,yval//2),self.radius)
        pygame.draw.rect(wn,(0,0,0),(int(xval//2-50),int(yval//2-75),100,20))
        pygame.draw.rect(wn,(100,100,255),(int(xval//2-50),int(yval//2-75),int(100*self.HP/self.OGHP),20))
        pygame.draw.rect(wn,(0,0,0),(int(xval//2-50),int(yval//2-50),100,20))
        pygame.draw.rect(wn,(100,100,255),(int(xval//2-50),int(yval//2-50),int(100*self.ammo/300),20))
        font = pygame.font.SysFont("Merriwheather bold",2*55//len(self.BRAWLER))
        drawntext = font.render(self.BRAWLER,False,(200,200,200))
        size = drawntext.get_size()
        wn.blit(drawntext,(int(xval//2-size[0]/2),int(yval//2-size[1]/2)))
        for i in self.bullets:
            pygame.draw.circle(wn,(30,30,255),(int(i[0]-self.x+xval//2),int(i[1]-self.y+yval//2)),int(i[7]))
        if self.HP<=0:
            self.buttons.FIND("END").CLICK()


        if won == True:
            self.buttons.FIND("END").visible = True
            self.HP = self.OGHP
        
    def DRAW(self,p):
        if self.ingame==3:
            self.GAME(p)
            self.MOVE()
        
        self.buttons.DRAW()
        self.buttons.FIND("PLAYERS").TEXT(str(self.playersfound[0])+" / "+str(self.playersfound[1]))
        self.buttons.FIND("GAMEMODE").TEXT("GAMEMODE: "+str(self.gamemode))
        
    def MOVE(self):
        key = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if key[pygame.K_UP] or key[pygame.K_w]:
            dy-=self.speed
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            dy+=self.speed
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx+=self.speed
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx-=self.speed
        if dx!=0 or dy!=0:
            dx,dy = (dx*self.speed/math.sqrt(dx**2+dy**2)),(dy*self.speed/math.sqrt(dx**2+dy**2))
        PLAYER.x+=int(dx)
        PLAYER.y+=int(dy)
        
        



PLAYER = PLAYER()

PLAYERS = []

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((IP, port))


def draw(PLAYERS):
    wn.fill((237,190,0))
    PLAYER.DRAW(PLAYERS)

run = True
clock = pygame.time.Clock()
while run:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            PLAYER.ingame = 1
    if PLAYER.ingame==1:
        PLAYERS = []
        client_sock.sendall(ENCODE([[1]]).encode())
    if PLAYER.ingame==2:
        PLAYERS = []
        client_sock.sendall(ENCODE([[2],[PLAYER.gamemode]]).encode())
    if PLAYER.ingame == 3:
        send = [[3],[PLAYER.gamemode],["PLAYER",int(PLAYER.x),int(PLAYER.y),PLAYER.BRAWLER,int(PLAYER.HP),int(PLAYER.OGHP),PLAYER.visible]]
        for i in PLAYER.bullets:
            send.append(["BULLET",int(i[0]),int(i[1]),int(i[7])])
        for i in PLAYER.hit:
            send.append(["HIT",int(i[0]),int(i[1])])
        client_sock.sendall(ENCODE(send).encode())
        PLAYER.hit = []
    g = PLAYER.ingame
    data = DECODE(client_sock.recv(4028).decode())
    if data[0][0]==2:
        PLAYER.playersfound = data[1]
    if data[0][0]==3:
        PLAYER.ingame = 3
        if g == 2:
            PLAYER.GAME_START()
            PLAYER.x = data[1][0]
            PLAYER.y = data[1][1]
            PLAYER.maps = data[2]
        else:
            PLAYERS = data[1:]
    draw(PLAYERS)
    pygame.display.update()
    
    clock.tick(fps)

    

pygame.quit()
