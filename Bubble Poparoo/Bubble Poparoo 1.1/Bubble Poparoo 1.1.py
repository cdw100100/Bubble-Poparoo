import pygame, random, sys, os
from pygame.locals import *

if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    # PyScreeze and Pillow needs to account for this to make accurate screenshots.
    # TODO - How does macOS and Linux handle monitor scaling?
    import ctypes
    try:
       ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.


#Path to program folder
basePath = os.path.dirname(sys.argv[0])+"\\"
#Initiating pygame and the pygame mixer for audio file
pygame.init()
pygame.mixer.init()
pop = pygame.mixer.Sound(basePath+"Sounds\\Pop.mp3")
pop.set_volume(0.4)
bMusic = pygame.mixer.Sound(basePath+"Sounds\\Sunset-Landscape.mp3")
bMusic.set_volume(0.5)
bMusic.play(-1,0)
#setting fps lock for game and startign clock (Both are needed for fps)
fps = 30
fClock = pygame.time.Clock()
#Setting up pygame display size and window
res = pygame.display.Info()
tv = pygame.display.set_mode((res.current_w, res.current_h), pygame.FULLSCREEN)
pygame.display.set_caption("Bubble Poparoo 1.1")
icImg = pygame.image.load(basePath+"Images\\Icon.png").convert_alpha()
pygame.display.set_icon(icImg)
#Setting background image
bgImg = pygame.transform.scale(pygame.image.load(basePath+"Images\\Background.png").convert_alpha(), (res.current_w, res.current_h))
#Bubble sprite class
class Bubble(pygame.sprite.Sprite):
    def __init__(self):
        #88 -Entry by my son Quintin Wargel 06:54:00 AM 07/02/22 Age 8 Months old.

        #Bubble settings for setup and creation
        self.radius = int((res.current_h*40)/100)
        self.imFrames = [pygame.image.load(basePath+"Images\\bPopF1.png").convert_alpha(),
                         pygame.image.load(basePath+"Images\\bPopF2.png").convert_alpha(),
                         pygame.image.load(basePath+"Images\\bPopF3.png").convert_alpha(),
                         pygame.image.load(basePath+"Images\\bPopF4.png").convert_alpha()]
        self.sImg = pygame.transform.scale(self.imFrames[0], (self.radius/2, self.radius/2))
        self.rect = self.sImg.get_rect()
        self.baseX = random.randint(0, res.current_w)
        self.way = 0
        self.rect.x = self.baseX
        self.rect.y = res.current_h+(self.radius*20)/100
        self.hide = False
        self.index = 0
        self.nTime = 0
        self.anit = False
    #Check if sprite has been clicked
    def clickCheck(self, pos):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            #Play music
            pop.play()
            #Play animation
            self.anit = True
            self.aGo()
    #Function to check if bubble pop animation should play
    def aGo(self):
        if self.anit:
            self.animate()
    #Function for controlling animation
    def animate(self):
        tNow = pygame.time.get_ticks()
        if (tNow > self.nTime):
            fDelay = 0.1
            self.nTime = tNow + fDelay

            self.index += 1
            if self.index >= len(self.imFrames):
                self.index = 0
                self.anit = False
                self.hide = True

        if self.hide == False:
            tv.blit(pygame.transform.scale(self.imFrames[self.index], (self.radius/2, self.radius/2)), (self.rect.x, self.rect.y))

    def move(self):
        #Placing/Moving sprite on the screen
        self.chCollision()
        if self.hide == False:
            if self.anit == False:
                tv.blit(self.sImg, (self.rect.x, self.rect.y))
            else:
                self.animate()
        #Bubble movment
        if self.rect.x > res.current_w-100:
            self.rect.x -= 1
            self.baseX -= 1
            self.way = 1
        elif self.rect.x < 0:
            self.rect.x += 1
            self.baseX += 1
            self.way = 0
            
        self.rect.y -=3
        if self.rect.x == self.baseX+20:
           self.way = 1
        elif self.rect.x == self.baseX-20:
            self.way = 0
        else:
            pass

        if self.way == 0:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        #If the bubble is above the screen and out of view then resets to bottom of screen
        if self.rect.y <= -self.radius-100:
            self.baseX = random.randint(0, res.current_w)
            self.rect.x = self.baseX
            self.rect.y = res.current_h+self.radius+10
            self.radius = random.randint(10,50)
            self.hide = False
    #Collision detection function
    def chCollision(self):
        for i in bList:
            if i != self:
                if self.rect.colliderect(i.rect):
                    if self.rect.x < i.rect.x:
                        self.baseX -= 3
                        self.rect.x -= 3
                    else:
                        self.baseX += 3
                        self.rect.x += 3
                    if i.rect.y > self.rect.y:
                        self.rect.y -= 3
                    else:
                        self.rect.y += 3
#Loop value and buuble list
go = True
sTime = 0
global bList
bList = []
#Main loop
while go:
    #Reseting the background
    tv.blit(bgImg, (0,0))
    #event checks
    for event in pygame.event.get():
        if event.type == QUIT:
            go = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                go = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for b in bList:
                b.clickCheck(event.pos)
    #Every 5 seconds spawn a new bubble if there is less than 8
    if pygame.time.get_ticks() > sTime:
        sTime += 2000
        if len(bList) < 20:
            bList.append(Bubble())
    #Looping through the bubble list to spawn/move them
    for b in bList:
        b.move()
    #Update the display and fps clock.
    pygame.display.update()
    fClock.tick(fps)
#Closing pygame and closing all functions
pygame.quit()
sys.exit()
