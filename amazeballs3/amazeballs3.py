import pgzrun
import map3d
from random import randint

player = {"x":3, "y":3, "frame":0, "sx":0, "sy":96,
          "moveX":0, "moveY":0, "queueX":0, "queueY":0,
          "moveDone":True, "movingNow":False, "animCounter":0, "dynamite":0}
enemy1 = {"x":13, "y":13, "frame":0, "sx":0, "sy":0,
          "moveX":0, "moveY":0, "queueX":0, "queueY":0,
          "moveDone":True, "movingNow":False, "animCounter":0}
enemy2 = {"x":25, "y":25, "frame":0, "sx":0, "sy":0,
          "moveX":0, "moveY":0, "queueX":0, "queueY":0,
          "moveDone":True, "movingNow":False, "animCounter":0}
OFFSETX = 368
OFFSETY = 300
timer = 0
mazeSolved = False

mapData = map3d.loadmap("maps/map1.json")

def draw(): # Pygame Zero draw function
    screen.fill((0, 0, 0))
    drawMap()
    screen.blit('title', (0, 0))
    screen.draw.text("TIME: "+str(timer) , topleft=(20, 80), owidth=0.5, ocolor=(255,255,0), color=(255,0,0) , fontsize=60)
    for l in range(player["dynamite"]): screen.blit("dmicon", (650+(l*32),80))
    if mazeSolved:
        screen.draw.text("MAZE SOLVED in " + str(timer) + " seconds!" , center=(400, 450), owidth=0.5, ocolor=(0,0,0), color=(0,255,0) , fontsize=60)


def update(): # Pygame Zero update function
    global player, timer
    mt = 0
    if player["moveDone"] == True:
        if keyboard.left: mt = doMove(player, -1, 0)
        if keyboard.right: mt = doMove(player, 1, 0)
        if keyboard.up: mt = doMove(player, 0, -1)
        if keyboard.down: mt = doMove(player, 0, 1)
    if mt == 4:
        mapData["data"][ player["y"] + player["queueY"]][ player["x"] + player["queueX"]] = 1
        player["dynamite"] += 1
    updateBall(player)
    updateBall(enemy1)
    updateBall(enemy2)
    updateEnemy(enemy1)
    updateEnemy(enemy2)

def on_key_down(key):
    if player["dynamite"] > 0 and key.name == "SPACE":
        player["dynamite"] -= 1
        for x in range(player["x"]-1, player["x"]+2):
            for y in range(player["y"]-1, player["y"]+2):
                mapData["data"][y][x] = 1

def timerTick():
    global timer
    if not mazeSolved:
        timer += 1

def drawMap():
    psx = OFFSETX
    psy = OFFSETY-32
    mx = psx - player["sx"]
    my = psy - player["sy"]+32
    
    for x in range(player["x"]-12, player["x"]+16):
        for y in range(player["y"]-12, player["y"]+16):
            if onMap(x,y):
                b = mapData["data"][y][x]
                td = findData(mapData["tiles"], "id", b)
                block = td["image"]
                bheight =  td["imageheight"]-34
                bx = (x*32)-(y*32) + mx
                by = (y*16)+(x*16) + my
                if -32 <= bx < 800 and 100 <= by < 620:
                    screen.blit(block, (bx, by - bheight))
                if x == player["x"] and y == player["y"]:
                    screen.blit("ball"+str(player["frame"]), (psx, psy))
                if x == enemy1["x"] and y == enemy1["y"]:
                    screen.blit("eball"+str(enemy1["frame"]), (bx + enemy1["sx"], (by-32)+enemy1["sy"]))
                if x == enemy2["x"] and y == enemy2["y"]:
                    screen.blit("eball"+str(enemy2["frame"]), (bx + enemy2["sx"], (by-32)+enemy2["sy"]))

def findData(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return dic
    return -1

def onMap(x,y):
    if 0 <= x < mapData["width"] and 0 <= y < mapData["height"]:
        return True
    return False

def doMove(p, x, y):
    global mazeSolved
    if onMap(p["x"]+x, p["y"]+y):
        mt = mapData["data"][p["y"]+y][p["x"]+x]
        if mt == 1 or mt == 3 or mt == 4:
            p.update({"queueX":x, "queueY":y, "moveDone":False})
            if mt == 3 and p == player:
                mazeSolved = True
        return mt

def updateEnemy(e):
    edirs = [[-1,0],[0,1],[1,0],[0,-1]]
    if e["moveX"] == 0 and e["moveY"] == 0:
        r = randint(0,3)
        if doMove(e, edirs[r][0], edirs[r][1]) == 2:
            moveBlock(e["x"]+edirs[r][0],e["y"]+edirs[r][1],edirs[r][0],edirs[r][1])
        e["sx"] = e["sy"] = 0
    else:
        if e["frame"] == 7 and e["movingNow"] == True:
            if e["sx"] == 12: e["sx"] -= 32
            if e["sx"] == -12: e["sx"] += 32
            if e["sy"] == 6: e["sy"] -= 16
            if e["sy"] == -6: e["sy"] += 16

def moveBlock(mx,my,dx,dy):
    if onMap(mx+dx,my+dy):
        d = mapData["data"][my+dy][mx+dx]
        if d == 1:
            mapData["data"][my+dy][mx+dx] = mapData["data"][my][mx]
            mapData["data"][my][mx] = 1
              
def updateBall(p):
    if p["movingNow"]:
        if p["moveX"] == -1: moveP(p,-1,-0.5)
        if p["moveX"] == 1: moveP(p,1,0.5)
        if p["moveY"] == -1: moveP(p,1,-0.5)
        if p["moveY"] == 1: moveP(p,-1,0.5)
    p["animCounter"] += 1
    if p["animCounter"] == 4:
        p["animCounter"] = 0
        p["frame"] += 1
        if p["frame"] > 7:
            p["frame"] = 0
        if p["frame"] == 4:
            if p["moveDone"] == False:
                if p["queueX"] != 0 or p["queueY"] !=0:
                    p.update({"moveX":p["queueX"], "moveY":p["queueY"], "queueX":0, "queueY":0, "movingNow": True})
            else:
                p.update({"moveDone":True, "moveX":0, "moveY":0, "movingNow":False})

        if p["frame"] == 7 and p["moveDone"] == False and p["movingNow"] == True:
            p["x"] += p["moveX"]
            p["y"] += p["moveY"]
            p["moveDone"] = True

def moveP(p,x,y):
    p["sx"] += x
    p["sy"] += y

clock.schedule_interval(timerTick, 1.0)
pgzrun.go()
