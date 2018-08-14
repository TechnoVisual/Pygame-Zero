import pgzrun
from random import randint
WIDTH = 800
HEIGHT = 600
gameStatus = 0
score = 0
player = Actor("player", (400, 550)) # Load in the player Actor image
aliens = []
bases = []
lasers = []
moveDelay = 30
moveCounter = 0
moveSequence = 0

def draw(): # Pygame Zero draw function
    screen.blit('background', (0, 0))
    player.draw()
    drawAliens()
    drawBases()
    screen.draw.text(str(score) , topright=(780, 10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)

def update(): # Pygame Zero update function
    global moveCounter
    checkKeys()
    if moveCounter == 0:
        updateAliens()
    moveCounter += 1
    if moveCounter == moveDelay:
        moveCounter = 0

def drawAliens():
    for a in range(len(aliens)):
        aliens[a].draw()

def drawBases():
    for b in range(len(bases)):
        bases[b].drawClipped()

def checkKeys():
    if keyboard.left:
        if player.x > 40:
            player.x -= 5
    if keyboard.right:
        if player.x < 760:
            player.x += 5
            
def checkBases():
    for b in range(len(bases)):
        if bases[b].height < 1:
            del bases[b]
            
def updateAliens():
    global moveSequence
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30:
        movex = -30
    if moveSequence == 10 or moveSequence == 30:
        movey = 30
    if moveSequence >10 and moveSequence < 30:
        movex = 30
    for a in range(len(aliens)):
        animate(aliens[a], pos=(aliens[a].x + movex, aliens[a].y + movey))
        if randint(0, 1) == 0:
            aliens[a].image = "alien1"
        else:
            aliens[a].image = "alien1b"
    moveSequence +=1
    if moveSequence == 40:
        moveSequence = 0

    bh = randint(0, len(bases)-1)    
    bases[bh].height -=2
    if bases[bh].height < 1:
        del bases[bh]
    
    #del aliens[randint(0, len(aliens)-1)]

def init():
    initAliens()
    initBases()

def initAliens():
    global aliens
    for a in range(18):
        aliens.append(Actor("alien1", (210+(a % 6)*80,50+(int(a/6)*64))))

def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y-self.height+30),(0,0,64,self.height))

def initBases():
    bc = 0
    for b in range(3):
        for p in range(3):
            bases.append(Actor("base1", midbottom=(150+(b*200)+(p*40),520)))
            bases[bc].drawClipped = drawClipped.__get__(bases[bc])
            bases[bc].height = 60
            bc +=1

init()
pgzrun.go()
