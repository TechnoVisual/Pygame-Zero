import pgzrun
from random import randint
import math
WIDTH = 800
HEIGHT = 600
gameStatus = 0
score = 0
player = Actor("player", (400, 550)) # Load in the player Actor image
player.status = 0
player.images = ["player","explosion1","explosion2","explosion3","explosion4","explosion5"]
aliens = []
bases = []
lasers = []
playerlasers = []
playerlaserCountdown = 0
moveDelay = 30
moveCounter = 0
moveSequence = 0

def draw(): # Pygame Zero draw function
    screen.blit('background', (0, 0))
    player.image = player.images[math.floor(player.status/6)]
    player.draw()
    drawLasers()
    drawAliens()
    drawBases()
    screen.draw.text(str(score) , topright=(780, 10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)

def update(): # Pygame Zero update function
    global moveCounter,player
    if player.status < 30:
        checkKeys()
        updateLasers()
        if moveCounter == 0:
            updateAliens()
        moveCounter += 1
        if moveCounter == moveDelay:
            moveCounter = 0
        if player.status > 0:
            player.status += 1
    if keyboard.RETURN:
        resetGame()

def drawAliens():
    for a in range(len(aliens)):
        aliens[a].draw()

def drawBases():
    for b in range(len(bases)):
        bases[b].drawClipped()

def drawLasers():
    for l in range(len(lasers)):
        lasers[l].draw()
    for l in range(len(playerlasers)):
        playerlasers[l].draw()

def checkKeys():
    global playerlaserCountdown, player
    if playerlaserCountdown > 0:
        playerlaserCountdown -= 1
    if keyboard.left:
        if player.x > 40:
            player.x -= 5
    if keyboard.right:
        if player.x < 760:
            player.x += 5
    if keyboard.space:
        if playerlaserCountdown == 0:
            playerlaserCountdown = 30
            playerlasers.append(Actor("laser2", (player.x,player.y-32)))
            playerlasers[len(playerlasers)-1].status = 0
            
def checkBases():
    for b in range(len(bases)):
        if l < len(bases):
            if bases[b].height < 5:
                del bases[b]

def updateLasers():
    global lasers, playerlasers, aliens
    for l in range(len(lasers)):
        lasers[l].y += 2
        checkLaserHit(l)
        if lasers[l].y > 600:
            lasers[l].status = 1
    for l in range(len(playerlasers)):
        playerlasers[l].y -= 5
        checkPlayerLaserHit(l)
        if playerlasers[l].y < 10:
            playerlasers[l].status = 1
    lasers = listCleanup(lasers)
    playerlasers = listCleanup(playerlasers)
    aliens = listCleanup(aliens)

def listCleanup(l):
    newList = []
    for i in range(len(l)):
        if l[i].status == 0:
            newList.append(l[i])
    return newList
    
def checkLaserHit(l):
    global player
    if player.colliderect(lasers[l]):
        player.status = 1
        lasers[l].status = 1
    for b in range(len(bases)):
        if bases[b].collideLaser(lasers[l]):
            bases[b].height -= 10
            lasers[l].status = 1

def checkPlayerLaserHit(l):
    global score
    for b in range(len(bases)):
        if bases[b].collideLaser(playerlasers[l]):
            playerlasers[l].status = 1
    for a in range(len(aliens)):
        if aliens[a].colliderect(playerlasers[l]):
            playerlasers[l].status = 1
            aliens[a].status = 1
            score += 1000
            
def updateAliens():
    global moveSequence, lasers
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
            if randint(0, 5) == 0:
                lasers.append(Actor("laser1", (aliens[a].x,aliens[a].y)))
                lasers[len(lasers)-1].status = 0
            
    moveSequence +=1
    if moveSequence == 40:
        moveSequence = 0


def init():
    initAliens()
    initBases()

def initAliens():
    global aliens
    for a in range(18):
        aliens.append(Actor("alien1", (210+(a % 6)*80,50+(int(a/6)*64))))
        aliens[a].status = 0

def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y-self.height+30),(0,0,64,self.height))

def collideLaser(self, other):
    return (
        self.x-32 < other.x+5 and
        self.y-self.height+30 < other.y and
        self.x+32 > other.x+5 and
        self.y-self.height+30 + self.height > other.y
    )

def initBases():
    bc = 0
    for b in range(3):
        for p in range(3):
            bases.append(Actor("base1", midbottom=(150+(b*200)+(p*40),520)))
            bases[bc].drawClipped = drawClipped.__get__(bases[bc])
            bases[bc].collideLaser = collideLaser.__get__(bases[bc])
            bases[bc].height = 60
            bc +=1
            
def resetGame():
    global aliens,lasers,playerlasers,score,player,bases,moveSequence
    aliens = []
    lasers = []
    playerlasers = []
    bases = []
    score = 0
    init()
    player.status = 0
    moveSequence
    
init()
pgzrun.go()
