import pgzrun
import gameinput
import gamemaps
from random import randint
from datetime import datetime
WIDTH = 600
HEIGHT = 660

player = Actor("pacman_o") # Load in the player Actor image
SPEED = 3

def draw(): # Pygame Zero draw function
    global pacDots, player
    screen.blit('header', (0, 0))
    screen.blit('colourmap', (0, 80))
    pacDotsLeft = 0
    for a in range(len(pacDots)):
        if pacDots[a].status == 0:
            pacDots[a].draw()
            pacDotsLeft += 1
        if pacDots[a].collidepoint((player.x, player.y)):
            pacDots[a].status = 1
    if pacDotsLeft == 0: player.status = 2
    drawGhosts()
    getPlayerImage()
    player.draw()
    if player.status == 1: screen.draw.text("GAME OVER" , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=40)
    if player.status == 2: screen.draw.text("YOU WIN!" , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=40)

def update(): # Pygame Zero update function
    global player, moveGhostsFlag, ghosts
    if player.status == 0:
        if moveGhostsFlag == 4: moveGhosts()
        for g in range(len(ghosts)):
            if ghosts[g].collidepoint((player.x, player.y)):
                player.status = 1
                pass
        if player.inputActive:
            gameinput.checkInput(player)
            gamemaps.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)

def init():
    global player
    initDots()
    initGhosts()
    player.x = 290
    player.y = 570
    player.status = 0
    inputUnLock()

def getPlayerImage():
    global player
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond%(500000/SPEED)/(100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey !=0):
        if a != 180:
            player.image = "pacman_c"
        else:
            player.image = "pacman_cr"
    else:
        if a != 180:
            player.image = "pacman_o"
        else:
            player.image = "pacman_or"
    player.angle = a

def drawGhosts():
    for g in range(len(ghosts)):
        if ghosts[g].x > player.x:
            ghosts[g].image = "ghost"+str(g+1)+"r"
        else:
            ghosts[g].image = "ghost"+str(g+1)
        ghosts[g].draw()

def moveGhosts():
    global moveGhostsFlag
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    moveGhostsFlag = 0
    for g in range(len(ghosts)):
        dirs = gamemaps.getPossibleDirection(ghosts[g])
        if ghostCollided(ghosts[g],g) and randint(0,3) == 0: ghosts[g].dir = 3
        if dirs[ghosts[g].dir] == 0 or randint(0,50) == 0:
            d = -1
            while d == -1:
                rd = randint(0,3)
                if dirs[rd] == 1:
                    d = rd
            ghosts[g].dir = d
        animate(ghosts[g], pos=(ghosts[g].x + dmoves[ghosts[g].dir][0]*20, ghosts[g].y + dmoves[ghosts[g].dir][1]*20), duration=1/SPEED, tween='linear', on_finished=flagMoveGhosts)

def flagMoveGhosts():
    global moveGhostsFlag
    moveGhostsFlag += 1

def ghostCollided(ga,gn):
    for g in range(len(ghosts)):
        if ghosts[g].colliderect(ga) and g != gn:
            return True
    return False
    
def initDots():
    global pacDots
    pacDots = []
    a = x = 0
    while x < 30:
        y = 0
        while y < 29:
            if gamemaps.checkDotPoint(10+x*20, 10+y*20):
                pacDots.append(Actor("dot",(10+x*20, 90+y*20)))
                pacDots[a].status = 0
                a += 1
            y += 1
        x += 1

def initGhosts():
    global ghosts, moveGhostsFlag
    moveGhostsFlag = 4
    ghosts = []
    g = 0
    while g < 4:
        ghosts.append(Actor("ghost"+str(g+1),(270+(g*20), 370)))
        ghosts[g].dir = randint(0, 3)
        g += 1

def inputLock():
    global player
    player.inputActive = False

def inputUnLock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True
    
init()
pgzrun.go()
