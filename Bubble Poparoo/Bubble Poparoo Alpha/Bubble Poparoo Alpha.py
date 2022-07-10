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
pygame.display.set_caption("Bubble Poparoo")

bx=random.randint(70, 1466)
x=bx
y=930
way = 0
radius=random.randint(50,100)

while True:
    tv.fill(white)
    circle = pygame.draw.circle(tv,blue,(x,y),radius)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if circle.collidepoint(event.pos):
                y = -100
                pygame.mixer.music.play()

    y -= 2

    if x == bx+20:
        way = 1
    elif x == bx-20:
        way = 0
    else:
        pass

    if way == 0:
        x += 1
    else:
        x -= 1

    if y <= 0:
        bx = random.randint(70, 1466)
        x = bx
        y = 930
        radius=random.randint(50,100)
    else:
        pass
    
    pygame.display.update()
    FramePerSec.tick(fps)
