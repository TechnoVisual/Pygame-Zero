import pgzrun
WIDTH = 800
HEIGHT = 600
gameStatus = 0
tileList = []
correctList = []
scrambleCountdown = 30
scrambleList = [2, 0, 2, 0, 3, 1, 1, 1, 3, 0, 0, 2, 1, 2, 1, 3, 3, 0, 3, 0, 2, 0, 2, 2, 1, 3, 1, 3, 3, 1, 2]

def draw(): # Pygame Zero draw function
    global gameStatus
    screen.fill((141, 172, 242))
    screen.blit('board', (150, 50))
    for t in range(15):
        tileList[t].draw()
    if (gameStatus == 3): screen.draw.text("Success!" , (315, 20), owidth=0.5, ocolor=(255,255,255), color=(128,64,0) , fontsize=60)
    if (gameStatus == 2): screen.draw.text("Please wait while we scramble the cat", (135, 540), owidth=0.5, ocolor=(255,255,255), color=(128,64,0) , fontsize=40)
    if (gameStatus <= 1): screen.draw.text("Click on a tile to move it or use the arrow keys", (95, 540), owidth=0.5, ocolor=(255,255,255), color=(128,64,0) , fontsize=40)

def update(): # Pygame Zero update function
    if (gameStatus == 0):
        if keyboard.left: findMoveTile("left")
        if keyboard.right: findMoveTile("right")
        if keyboard.up: findMoveTile("up")
        if keyboard.down: findMoveTile("down")

def on_mouse_down(pos):
    if (gameStatus == 0):
        doLock()
        for t in range(15):
            if tileList[t].collidepoint(pos):
                m = moveTile(tileList[t])
                if(m != False):
                    animate(tileList[t],on_finished=releaseLock, pos=(tileList[t].x+m[1], tileList[t].y+m[2]))
                    return True
        releaseLock()

def findMoveTile(moveDirection):
    doLock()
    for t in range(15):
        m = moveTile(tileList[t])
        if(m != False):
            if(m[0] == moveDirection):
                animate(tileList[t],on_finished=releaseLock, pos=(tileList[t].x+m[1], tileList[t].y+m[2]))
                return True
    releaseLock()
    return False

def releaseLock():
    global gameStatus
    if(gameStatus == 2): scrambleCat()
    else: gameStatus = checkSuccess()

def doLock():
    global gameStatus
    gameStatus = 1

def checkSuccess():
    for t in range(15):
        if(tileList[t].x != correctList[t][0] or tileList[t].y != correctList[t][1]):
            return 0
    return 3	# we have success!

def makeTiles():
    global tileList, correctList
    xoffset = 251
    yoffset = 151
    x = y = c = 0
    while y < 4:
        while x < 4:
            if(c < 15):
                tileList.append(Actor("img"+str(c), pos = (xoffset+(x*100),yoffset+(y*100))))
                correctList.append((xoffset+(x*100),yoffset+(y*100)))
            c += 1
            x += 1
        x = 0
        y += 1
    scrambleCat()    

def scrambleCat():
    global gameStatus, scrambleCountdown, scrambleList
    tileDirs = ["left", "right", "up", "down"]
    if(scrambleCountdown > 0):
        mt = False
        while(mt == False):
            mt = findMoveTile(tileDirs[scrambleList[scrambleCountdown]])
            scrambleCountdown -= 1
        gameStatus = 2
    else:
        gameStatus = 0

def moveTile(tile):
    borderRight = 551
    borderLeft = 251
    borderTop = 151
    borderBottom = 451
    rValue = False
    if(tile.x < borderRight): # can we go right?
        tile.x += 1
        if(not checkCollide(tile)): rValue = "right", 100, 0
        tile.x -= 1
    if(tile.x > borderLeft): # can we go left?
        tile.x -= 1
        if(not checkCollide(tile)): rValue = "left", -100, 0
        tile.x += 1
    if(tile.y < borderBottom): # can we go down?
        tile.y += 1
        if(not checkCollide(tile)): rValue = "down", 0, 100
        tile.y -= 1
    if(tile.y > borderTop): # can we go up?
        tile.y -= 1
        if(not checkCollide(tile)): rValue = "up", 0, -100
        tile.y += 1
    return rValue

def checkCollide(tile):
    for t in range(15):
        if tile.colliderect(tileList[t]) and tile != tileList[t]: return True
    return False

makeTiles()  
pgzrun.go()
