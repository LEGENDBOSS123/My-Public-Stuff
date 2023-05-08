import pygame
from random_word import RandomWords
pygame.init()
wn = pygame.display.set_mode((1500,750))

def refill():
    wn.fill((255,255,255))
def check(chosen_word, alphabet):
    for i in chosen_word:
        if i not in alphabet:
            self.chosen_word = self.words.get_random_word(hasDictionaryDef="true", maxLength=6)
            self.chosen_word = self.chosen_word.upper()
            check(chosen_word,alphabet)
class HANGMAN():
    def __init__(self):
        self.tries = 0
        self.corrects = 0
        self.close = False
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.words = RandomWords()
        self.chosen_word = self.words.get_random_word(hasDictionaryDef="true", maxLength=6)
        self.chosen_word = self.chosen_word.upper()
        check(self.chosen_word, self.alphabet)
        
        
        self.display_word = [" _ "]*len(self.chosen_word)
        
        self.K_alphabet = [pygame.K_a,
                           pygame.K_b,
                           pygame.K_c,
                           pygame.K_d,
                           pygame.K_e,
                           pygame.K_f,
                           pygame.K_g,
                           pygame.K_h,
                           pygame.K_i,
                           pygame.K_j,
                           pygame.K_k,
                           pygame.K_l,
                           pygame.K_m,
                           pygame.K_n,
                           pygame.K_o,
                           pygame.K_p,
                           pygame.K_q,
                           pygame.K_r,
                           pygame.K_s,
                           pygame.K_t,
                           pygame.K_u,
                           pygame.K_v,
                           pygame.K_w,
                           pygame.K_x,
                           pygame.K_y,
                           pygame.K_z]
    def what_to_do_when_key_gets_pressed(self,key):
        if key in self.chosen_word:
            for i in range(len(self.chosen_word)):
                if self.chosen_word[i] == key:
                    self.display_word[i] = " "+key+" "
                    self.corrects+=1
        else:
            self.tries+=1
            
    def str_list(self, List):
        string = ""
        for i in List:
            string+=str(i)
        return string
    def str_list2(self, List):
        string = ""
        for i in List:
            string+="  "
            string+=str(i)
            string+="  "
        return string
    def check_end_game(self):
        if self.tries>=6:
            font = pygame.font.Font("freesansbold.ttf",75)
            text = font.render("YOU LOST", True, (0,0,0),(255,255,255))
            recttext = text.get_rect()
            
            recttext.center = ((750,600))
            wn.blit(text, recttext)
            self.draw_HM()
            self.close = True
            pygame.display.update()
            pygame.time.delay(2000)
            refill()
            font = pygame.font.Font("freesansbold.ttf",32)
            text = font.render("THE WORD WAS "+self.chosen_word, True, (0,0,0),(255,255,255))
            recttext = text.get_rect()
            
            recttext.center = ((750,600))
            wn.blit(text, recttext)
        elif self.corrects == len(self.chosen_word):
            pygame.time.delay(2000)
            font = pygame.font.Font("freesansbold.ttf",75)
            text = font.render("YOU WON", True, (0,0,0),(255,255,255))
            recttext = text.get_rect()
            
            recttext.center = ((750,600))
            wn.blit(text, recttext)
            self.draw_HM()
            self.close = True
        else:
            self.draw()
    def key_check(self):
        key = pygame.key.get_pressed()
        for i in range(26):
            
            if key[self.K_alphabet[i]] and self.alphabet[i]!=" ":
                self.what_to_do_when_key_gets_pressed(self.alphabet[i])
                self.alphabet[i] = " "
    def write(self):
        font = pygame.font.Font("freesansbold.ttf",32)
        text = font.render(self.str_list(self.display_word), True, (0,0,0),(255,255,255))
        recttext = text.get_rect()
        
        recttext.center = ((750,600))
        wn.blit(text, recttext)
        for i in range(26):
            font = pygame.font.Font("freesansbold.ttf",20)
            text = font.render(self.str_list2(self.alphabet), True, (0,0,0),(255,255,255))
            recttext = text.get_rect()
            
            recttext.center = ((750,700))
            wn.blit(text, recttext)
    def draw_HM(self):
        pygame.draw.line(wn,(0,0,0),(0,500),(1500,500),10)
        pygame.draw.line(wn,(0,0,0),(925,500),(925,50),10)
        pygame.draw.line(wn,(0,0,0),(925,50),(500,50),10)
        pygame.draw.line(wn,(0,0,0),(500,50),(500,100),10)
        if self.tries>=1:
            pygame.draw.circle(wn,(0,0,0),(500,150),50,7)
            pygame.draw.circle(wn,(0,0,0),(485,130),5)
            pygame.draw.circle(wn,(0,0,0),(515,130),5)
            pygame.draw.circle(wn,(0,0,0),(500,145),5)
            pygame.draw.line(wn,(0,0,0),(475,160),(525,160),5)
        if self.tries>=2:
            pygame.draw.line(wn,(0,0,0),(500,200),(500,350),5)
        if self.tries>=3:
            pygame.draw.line(wn,(0,0,0),(500,350),(550,475),5)
        if self.tries>=4:
            pygame.draw.line(wn,(0,0,0),(500,270),(400,225),5)
        if self.tries>=5:
            pygame.draw.line(wn,(0,0,0),(500,350),(450,475),5)
        if self.tries>=6:
            pygame.draw.line(wn,(0,0,0),(500,270),(600,225),5)
    def draw(self):
        self.key_check()
        
        
        self.draw_HM()
        self.write()

HM = HANGMAN()
run = True

def draw_screen():
    refill()
    HM.check_end_game()
while run:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    draw_screen()
    pygame.display.update()
    if HM.close == True:
        run = False
        pygame.time.delay(1000)
pygame.quit()
