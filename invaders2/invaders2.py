import pgzrun, math, re, time
from random import randint
player = Actor("player", (400, 550))
boss = Actor("boss")
gameStatus = 0
highScore = []

def draw(): # Pygame Zero draw function
    screen.blit('background', (0, 0))
    if gameStatus == 0: # display the title page
        drawCentreText("PYGAME ZERO INVADERS\n\n\nType your name then\npress Enter to start\n(arrow keys move, space to fire)")
        screen.draw.text(player.name , center=(400, 500), owidth=0.5, ocolor=(255,0,0), color=(0,64,255) , fontsize=60)
    if gameStatus == 1: # playing the game
        player.image = player.images[math.floor(player.status/6)]
        player.draw()
        if boss.active: boss.draw()
        drawLasers()
        drawAliens()
        drawBases()
        screen.draw.text(str(score) , topright=(780, 10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)
        screen.draw.text("LEVEL " + str(level) , midtop=(400, 10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)
        drawLives()
        if player.status >= 30:
            if player.lives > 0:
                drawCentreText("YOU WERE HIT!\nPress Enter to re-spawn")
            else:
                drawCentreText("GAME OVER!\nPress Enter to continue")
        if len(aliens) == 0 :
            drawCentreText("LEVEL CLEARED!\nPress Enter to go to the next level")
    if gameStatus == 2: # game over show the leaderboard
        drawHighScore()

def drawCentreText(t):
    screen.draw.text(t , center=(400, 300), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)
    
def update(): # Pygame Zero update function
    global moveCounter, player, gameStatus, lasers, level, boss
    if gameStatus == 0:
        if keyboard.RETURN and player.name != "": gameStatus = 1
    if gameStatus == 1:
        if player.status < 30 and len(aliens) > 0:
            checkKeys()
            updateLasers()
            updateBoss()
            if moveCounter == 0: updateAliens()
            moveCounter += 1
            if moveCounter == moveDelay: moveCounter = 0
            if player.status > 0:
                player.status += 1
                if player.status == 30:
                    player.lives -= 1
        else:
            if keyboard.RETURN:
                if player.lives > 0:
                    player.status = 0
                    lasers = []
                    if len(aliens) == 0:
                        level += 1
                        boss.active = False
                        initAliens()
                        initBases()
                else:
                    readHighScore()
                    gameStatus = 2
                    writeHighScore()
    if gameStatus == 2:
        if keyboard.ESCAPE:
            init()
            gameStatus = 0
            
def on_key_down(key):
    global player
    if gameStatus == 0 and key.name != "RETURN":
        if len(key.name) == 1:
            player.name += key.name
        else:
            if key.name == "BACKSPACE":
                player.name = player.name[:-1]
    
def readHighScore():
    global highScore, score, player
    highScore = []
    try:
        hsFile = open("highscores.txt", "r")
        for line in hsFile:
            highScore.append(line.rstrip())
    except:
        pass
    highScore.append(str(score)+ " " + player.name)
    highScore.sort(key=natural_key, reverse=True)

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def writeHighScore():
    global highScore
    hsFile = open("highscores.txt", "w")
    for line in highScore:
        hsFile.write(line + "\n")

def drawHighScore():
    global highScore
    y = 0
    screen.draw.text("TOP SCORES", midtop=(400, 30), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)
    for line in highScore:
        if y < 400:
            screen.draw.text(line, midtop=(400, 100+y), owidth=0.5, ocolor=(0,0,255), color=(255,255,0) , fontsize=50)
            y += 50
    screen.draw.text("Press Escape to play again" , center=(400, 550), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)

def drawLives():
    for l in range(player.lives): screen.blit("life", (10+(l*32),10))

def drawAliens():
    for a in range(len(aliens)): aliens[a].draw()

def drawBases():
    for b in range(len(bases)): bases[b].drawClipped()

def drawLasers():
    for l in range(len(lasers)): lasers[l].draw()

def checkKeys():
    global player, score
    if keyboard.left:
        if player.x > 40: player.x -= 5
    if keyboard.right:
        if player.x < 760: player.x += 5
    if keyboard.space:
        if player.laserActive == 1:
            sounds.gun.play()
            player.laserActive = 0
            clock.schedule(makeLaserActive, 1.0)
            lasers.append(Actor("laser2", (player.x,player.y-32)))
            lasers[len(lasers)-1].status = 0
            lasers[len(lasers)-1].type = 1
            score -= 100

def makeLaserActive():
    global player
    player.laserActive = 1
    
def checkBases():
    for b in range(len(bases)):
        if l < len(bases):
            if bases[b].height < 5:
                del bases[b]

def updateLasers():
    global lasers, aliens
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += 2
            checkLaserHit(l)
            if lasers[l].y > 600: lasers[l].status = 1
        if lasers[l].type == 1:
            lasers[l].y -= 5
            checkPlayerLaserHit(l)
            if lasers[l].y < 10: lasers[l].status = 1
    lasers = listCleanup(lasers)
    aliens = listCleanup(aliens)

def listCleanup(l):
    newList = []
    for i in range(len(l)):
        if l[i].status == 0: newList.append(l[i])
    return newList
    
def checkLaserHit(l):
    global player
    if player.collidepoint((lasers[l].x, lasers[l].y)):
        sounds.explosion.play()
        player.status = 1
        lasers[l].status = 1
    for b in range(len(bases)):
        if bases[b].collideLaser(lasers[l]):
            bases[b].height -= 10
            lasers[l].status = 1

def checkPlayerLaserHit(l):
    global score, boss
    for b in range(len(bases)):
        if bases[b].collideLaser(lasers[l]): lasers[l].status = 1
    for a in range(len(aliens)):
        if aliens[a].collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = 1
            aliens[a].status = 1
            score += 1000
    if boss.active:
        if boss.collidepoint((lasers[l].x, lasers[l].y)):
            lasers[l].status = 1
            boss.active = 0
            score += 5000
        
def updateAliens():
    global moveSequence, lasers, moveDelay
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30: movex = -15
    if moveSequence == 10 or moveSequence == 30:
        movey = 40 + (5*level)
        moveDelay -= 1
    if moveSequence >10 and moveSequence < 30: movex = 15
    for a in range(len(aliens)):
        animate(aliens[a], pos=(aliens[a].x + movex, aliens[a].y + movey), duration=0.5, tween='linear')
        if randint(0, 1) == 0:
            aliens[a].image = "alien1"
        else:
            aliens[a].image = "alien1b"
            if randint(0, 5) == 0:
                lasers.append(Actor("laser1", (aliens[a].x,aliens[a].y)))
                lasers[len(lasers)-1].status = 0
                lasers[len(lasers)-1].type = 0
                sounds.laser.play()
        if aliens[a].y > 500 and player.status == 0:
            sounds.explosion.play()
            player.status = 1
            player.lives = 1
    moveSequence +=1
    if moveSequence == 40: moveSequence = 0

def updateBoss():
    global boss, level, player, lasers
    if boss.active:
        boss.y += (0.3*level)
        if boss.direction == 0: boss.x -= (1* level)
        else: boss.x += (1* level)
        if boss.x < 100: boss.direction = 1
        if boss.x > 700: boss.direction = 0
        if boss.y > 500:
            sounds.explosion.play()
            player.status = 1
            boss.active = False
        if randint(0, 30) == 0:
            lasers.append(Actor("laser1", (boss.x,boss.y)))
            lasers[len(lasers)-1].status = 0
            lasers[len(lasers)-1].type = 0
    else:
        if randint(0, 800) == 0:
            boss.active = True
            boss.x = 800
            boss.y = 100
            boss.direction = 0

def init():
    global lasers, score, player, moveSequence, moveCounter, moveDelay, level, boss
    initAliens()
    initBases()
    moveCounter = moveSequence = player.status = score = player.laserCountdown = 0
    lasers = []
    moveDelay = 30
    boss.active = False
    player.images = ["player","explosion1","explosion2","explosion3","explosion4","explosion5"]
    player.laserActive = 1
    player.lives = 3
    player.name = ""
    level = 1

def initAliens():
    global aliens, moveCounter, moveSequence
    aliens = []
    moveCounter = moveSequence = 0
    for a in range(18):
        aliens.append(Actor("alien1", (210+(a % 6)*80,100+(int(a/6)*64))))
        aliens[a].status = 0

def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y-self.height+30),(0,0,64,self.height))

def collideLaser(self, other):
    return (
        self.x-20 < other.x+5 and
        self.y-self.height+30 < other.y and
        self.x+32 > other.x+5 and
        self.y-self.height+30 + self.height > other.y
    )

def initBases():
    global bases
    bases = []
    bc = 0
    for b in range(3):
        for p in range(3):
            bases.append(Actor("base1", midbottom=(150+(b*200)+(p*40),520)))
            bases[bc].drawClipped = drawClipped.__get__(bases[bc])
            bases[bc].collideLaser = collideLaser.__get__(bases[bc])
            bases[bc].height = 60
            bc +=1
    
init()
pgzrun.go()
