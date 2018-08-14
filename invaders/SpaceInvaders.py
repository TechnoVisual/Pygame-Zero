import pgzrun

WIDTH = 800
HEIGHT = 600
gameStatus = 0
score = 0
player = Actor("player", (400, 550)) # Load in the player Actor image
aliens = []
bases = []
lasers = []
moveDelay = 10
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
        updateShips()
    moveCounter += 1
    if moveCounter == moveDelay:
        moveCounter = 0

def drawAliens():
    pass

def drawBases():
    for b in range(3):
        for p in range(3):
            bases[b][p].draw()

def checkKeys():
    if keyboard.left:
        if player.x > 40:
            player.x -= 5
    if keyboard.right:
        if player.x < 760:
            player.x += 5

def updateShips():
    global moveSequence
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30:
        movex = -10
    if moveSequence == 10 or moveSequence == 30:
        movey = 10
    if moveSequence >10 and moveSequence < 30:
        movex = 10
    for a in range(18):
        animate(aliens[a], pos=(aliens[a].x + movex, aliens[a].y + movey))
    moveSequence +=1
    if moveSequence == 40:
        moveSequence = 0

def init():
    initAliens()
    initBases()

def initAliens():
    global aliens
    for a in range(18):
        aliens.append(Actor("alien1", (200+(a % 6)*64,50+(int(a/3)*32))))

def initBases():
    for b in range(3):
        bases.append([])
        for p in range(3):
            bases[b].append(Actor("base1", (150+(b*200)+(p*40),480)))

init()
pgzrun.go()
