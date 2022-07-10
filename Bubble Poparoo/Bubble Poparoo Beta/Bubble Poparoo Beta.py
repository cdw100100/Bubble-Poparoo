import random, pygame, sys, os
from pygame.locals import *

bPath = os.path.dirname(sys.argv[0])+"\\"
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(bPath+"Sounds\\Pop.mp3")
pygame.mixer.music.set_volume(0.7)

fps = 30
FramePerSec = pygame.time.Clock()

blue  = (0, 0, 255)
red   = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

tv = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
tv.fill(white)
pygame.display.set_caption("Bubble Poparoo Beta")
bg = pygame.image.load(bPath+"Images\\Bubble.png").convert_alpha()
pygame.display.set_icon(bg)

class Bubble(pygame.sprite.Sprite):
   def __init__(self):

       self.radius = random.randint(150,400)
       self.image = pygame.Surface([self.radius/2,self.radius/2])
       self.image.fill(blue)
       self.image = pygame.image.load(bPath+"Images\\Bubble.png").convert_alpha()
       self.image = pygame.transform.scale(self.image,(self.radius, self.radius))
       self.rect = self.image.get_rect()
       self.bx = random.randint(70, 1466)
       self.way = 0
       self.rect.x = self.bx
       self.rect.y = 930

   def move(self):
       #circle = pygame.draw.circle(tv,blue, self.rect.center, self.radius)
       tv.blit(self.image, (self.rect.x,self.rect.y))
        
       self.rect.y -= 3
       if self.rect.x == self.bx+20:
           self.way = 1
       elif self.rect.x == self.bx-20:
           self.way = 0
       else:
           pass

       if self.way == 0:
           self.rect.x += 1
       else:
           self.rect.x -= 1

       if self.rect.y <= -50:
           self.bx = random.randint(70, 1466)
           self.rect.x = self.bx
           self.rect.y = 930
           self.radius=random.randint(150,400)
       else:
           pass


bubbleList = []

nBubble = 0
while True:
    tv.fill(white)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for b in bubbleList:
                if b.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.music.play()
                    b.color=white
                    b.rect.y = -1000

    if pygame.time.get_ticks() > nBubble:
        nBubble += 5000

        if len(bubbleList) < 8:
            bubbleList.append(Bubble())
        else:
            pass
        
    for b in bubbleList:
        b.move()
    
    pygame.display.update()
    FramePerSec.tick(fps)
