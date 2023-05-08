#!/usr/bin/env python3
import pygame
import random
pygame.init()
wn = pygame.display.set_mode((500,500))
wn.fill((255,255,255))
def factorial(num):
    fact_val = 1
    if num < 1:
        fact_val = 1
    else:
        for i in range(num):
            fact_val *= (i + 1)

    return fact_val

def permute(num):
    rand_rank = random.randint(0, factorial(num) - 1)
    return find_permute_for_rank(num, rand_rank)


def find_permute_for_rank(num, rank):
    permute_list = []
    list_of_num = []
    for i in range(num):
        list_of_num.append(i+1)
    while num > 0:
        new_fact = factorial(num - 1)
        candidate_num =  rank // new_fact
        candidate = list_of_num[candidate_num]
        remainder = rank - (candidate_num * new_fact)
        permute_list.append(candidate)
        list_of_num.remove(candidate)
        num = num - 1
        rank = remainder

    return permute_list




class GAME(object):
    def __init__(self):
        self.focus = False
        self.win = False
        self.click = pygame.mouse.get_pressed()
        self.win_count = 0
        self.mouse_x,self.mouse_y = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
    def win_check(self):
        if self.win == True:
            pygame.draw.rect(wn,(0,0,0),(0,0,500,500))
            font = pygame.font.Font("freesansbold.ttf",75)
            text = font.render("YOU WON", True, (255,255,255),(0,0,0))
            recttext = text.get_rect()
            recttext.center = (250,250)
            wn.blit(text, recttext)
        '''elif self.win == "lost":
            pygame.draw.rect(wn,(0,0,0),(0,0,500,500))
            font = pygame.font.Font("freesansbold.ttf",75)
            text = font.render("YOU LOST", True, (255,255,255),(0,0,0))
            recttext = text.get_rect()
            recttext.center = (250,250)
            wn.blit(text, recttext)'''
    def check(self):
        for each_box in boxes:
            if each_box.answer == each_box.your_answer:
                self.win_count+=1
        if self.win_count >= 9:
            self.win = True
        else:
            self.win_count = 0
            self.win = "lost"
            
    def restore(self):
        self.click = pygame.mouse.get_pressed()
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
            
    def buttonclick(self):
        pygame.draw.rect(wn,(0,0,0),(350,350,100,50))
        font = pygame.font.Font("freesansbold.ttf",20)
        text = font.render("SUBMIT", True, (255,255,255),(0,0,0))
        recttext = text.get_rect()
        recttext.center = (400,375)
        wn.blit(text, recttext)
        self.restore()
        if self.mouse_x>=350 and self.mouse_x<=450 and self.mouse_y>=350 and self.mouse_y<=400 and self.click[0] == 1:
            
            self.check()
    def draw(self):
        font = pygame.font.Font("freesansbold.ttf",32)
        
        text = font.render(str(thelist[0]*thelist[1]*thelist[2]), True, (0,0,0),(255,255,255))
        recttext = text.get_rect()
        recttext.center = (350,50)
        wn.blit(text, recttext)

        text = font.render(str(thelist[3]*thelist[4]*thelist[5]), True, (0,0,0),(255,255,255))
        recttext = text.get_rect()
        recttext.center = (350,150)
        wn.blit(text, recttext)

        text = font.render(str(thelist[6]*thelist[7]*thelist[8]), True, (0,0,0),(255,255,255))
        recttext = text.get_rect()
        recttext.center = (350,250)
        wn.blit(text, recttext)

        text = font.render(str(thelist[0]*thelist[3]*thelist[6]), True, (0,0,0),(255,255,255))
        recttext = text.get_rect()
        recttext.center = (50,350)
        wn.blit(text, recttext)

        text = font.render(str(thelist[1]*thelist[4]*thelist[7]), True, (0,0,0),(255,255,255))
        recttext = text.get_rect()
        recttext.center = (150,350)
        wn.blit(text, recttext)

        text = font.render(str(thelist[2]*thelist[5]*thelist[8]), True, (0,0,0),(255,255,255))
        recttext = text.get_rect()
        recttext.center = (250,350)
        wn.blit(text, recttext)
        
        pygame.draw.line(wn,(0,0,0),(0,0),(0,300),4)
        pygame.draw.line(wn,(0,0,0),(300,0),(300,300),3)
        pygame.draw.line(wn,(0,0,0),(0,0),(300,0),4)
        pygame.draw.line(wn,(0,0,0),(0,300),(300,300),3)

        pygame.draw.line(wn,(0,0,0),(0,100),(300,100),3)
        pygame.draw.line(wn,(0,0,0),(0,200),(300,200),3)

        pygame.draw.line(wn,(0,0,0),(100,0),(100,300),3)
        pygame.draw.line(wn,(0,0,0),(200,0),(200,300),3)
        
        
class BOX(object):
    def __init__(self,num,thelist):
        self.num = num
        self.answer = thelist[num-1]
        self.your_answer = None
        self.x_min = "not set YET"
        self.x_max = "not set YET"
        self.y_min = "not set YET"
        self.y_max = "not set YET"
        self.typenumber = ""
        if self.num == 1:
            self.x_min,self.x_max = 0,100
            self.y_min,self.y_max = 0,100
        if self.num == 2:
            self.x_min,self.x_max = 100,200
            self.y_min,self.y_max = 0,100
        if self.num == 3:
            self.x_min,self.x_max = 200,300
            self.y_min,self.y_max = 0,100
        if self.num == 4:
            self.x_min,self.x_max = 0,100
            self.y_min,self.y_max = 100,200
        if self.num == 5:
            self.x_min,self.x_max = 100,200
            self.y_min,self.y_max = 100,200
        if self.num == 6:
            self.x_min,self.x_max = 200,300
            self.y_min,self.y_max = 100,200
        if self.num == 7:
            self.x_min,self.x_max = 00,100
            self.y_min,self.y_max = 200,300
        if self.num == 8:
            self.x_min,self.x_max = 100,200
            self.y_min,self.y_max = 200,300
        if self.num == 9:
            self.x_min,self.x_max = 200,300
            self.y_min,self.y_max = 200,300
            
    def work(self):
        game.restore()
        if game.mouse_x<self.x_max and game.mouse_x>self.x_min and game.mouse_y<self.y_max and game.mouse_y>self.y_min:
            if game.click[0] == 1:
                game.focus = self.num
        keys = pygame.key.get_pressed()
        font = pygame.font.Font("freesansbold.ttf",75)
        if game.focus == self.num:
            if keys[pygame.K_1]:
                self.typenumber = "1"
                self.your_answer = 1
            if keys[pygame.K_2]:
                self.typenumber = "2"
                self.your_answer = 2
            if keys[pygame.K_3]:
                self.typenumber = "3"
                self.your_answer = 3
            if keys[pygame.K_4]:
                self.typenumber = "4"
                self.your_answer = 4
            if keys[pygame.K_5]:
                self.typenumber = "5"
                self.your_answer = 5
            if keys[pygame.K_6]:
                self.typenumber = "6"
                self.your_answer = 6
            if keys[pygame.K_7]:
                self.typenumber = "7"
                self.your_answer = 7
            if keys[pygame.K_8]:
                self.typenumber = "8"
                self.your_answer = 8
            if keys[pygame.K_9]:
                self.typenumber = "9"
                self.your_answer = 9
            if keys[pygame.K_BACKSPACE]:
                self.typenumber = ""
                self.your_answer = None


                
        text = font.render(self.typenumber, True, (0,0,0),(255,255,255))
        recttext = text.get_rect()
        recttext.center = (self.x_min+(self.x_max-self.x_min)//2,self.y_min+(self.y_max-self.y_min)//2)
        wn.blit(text, recttext)

thelist = permute(9)
game = GAME()
box1 = BOX(1,thelist)
box2 = BOX(2,thelist)
box3 = BOX(3,thelist)
box4 = BOX(4,thelist)
box5 = BOX(5,thelist)
box6 = BOX(6,thelist)
box7 = BOX(7,thelist)
box8 = BOX(8,thelist)
box9 = BOX(9,thelist)
boxes = []
boxes.append(box1)
boxes.append(box2)
boxes.append(box3)
boxes.append(box4)
boxes.append(box5)
boxes.append(box6)
boxes.append(box7)
boxes.append(box8)
boxes.append(box9)
def draw(wn):
    wn.fill((255,255,255))
    game.draw()
    
    for each_box in boxes:
        each_box.work()
    game.buttonclick()
    game.win_check()
    
run = True
while run:
    pygame.time.delay(20)
    draw(wn)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    

    

    pygame.display.update()

pygame.quit()
     
