import pgzrun
from random import randint
import math
WIDTH = 800
HEIGHT = 600

myButtons = []
myButtons.append(Actor('redunlit', bottomright=(400,270)))
myButtons[0].state = False
myButtons.append(Actor('greenunlit',bottomleft=(400,270)))
myButtons[1].state = False
myButtons.append(Actor('blueunlit',topright=(400,270)))
myButtons[2].state = False
myButtons.append(Actor('yellowunlit',topleft=(400,270)))
myButtons[3].state = False
buttonsLit = ['redlit', 'greenlit', 'bluelit', 'yellowlit']
buttonsUnlit = ['redunlit', 'greenunlit', 'blueunlit', 'yellowunlit']
playButton = Actor('play', pos=(400,540))
buttonList = []
playPosition = 0
playingAnimation = False
gameCountdown = -1
LOOPDELAY = 80
score = 0
playerInput = []
signalScore = False
gameStarted = False

def draw(): # Pygame Zero draw function
    global playingAnimation, score
    screen.fill((30, 10, 30))
    for b in myButtons: b.draw()
    if gameStarted:
        screen.draw.text("Score : " + str(score), (310, 540), owidth=0.5, ocolor=(255,255,255), color=(255,128,0) , fontsize=60)
    else:
        playButton.draw()
        screen.draw.text("Play", (370, 525), owidth=0.5, ocolor=(255,255,255), color=(255,128,0) , fontsize=40)
        if score > 0:
            screen.draw.text("Final Score : " + str(score), (250, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0) , fontsize=60)
        else:
            screen.draw.text("Press Play to Start", (220, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0) , fontsize=60)
    if playingAnimation or gameCountdown > 0:
        screen.draw.text("Watch", (330, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0) , fontsize=60)
    if not playingAnimation and gameCountdown == 0:
        screen.draw.text("Now You", (310, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0) , fontsize=60)
    
def update(): # Pygame Zero update function
    global myButtons, playingAnimation, playPosition, gameCountdown
    if playingAnimation:
        playPosition += 1
        listpos = math.floor(playPosition/LOOPDELAY)
        if listpos == len(buttonList):
            playingAnimation = False
            clearButtons()
        else:   
            litButton = buttonList[listpos]
            if playPosition%LOOPDELAY > LOOPDELAY/2: litButton = -1
            bcount = 0
            for b in myButtons:
                if litButton == bcount: b.state = True
                else: b.state = False
                bcount += 1
    bcount = 0
    for b in myButtons:
        if b.state == True: b.image = buttonsLit[bcount]
        else: b.image = buttonsUnlit[bcount]
        bcount += 1
    if gameCountdown > 0:
        gameCountdown -=1
        if gameCountdown == 0:
            addButton()
            playerInput.clear()

def gameOver():
    global gameStarted, gameCountdown, playerInput, buttonList
    gameStarted = False
    gameCountdown = -1
    playerInput.clear()
    buttonList.clear()
    clearButtons()

def checkPlayerInput():
    global playerInput, gameStarted, score, buttonList, gameCountdown, signalScore
    ui = 0
    while ui < len(playerInput):
        if playerInput[ui] != buttonList[ui]: gameOver()
        ui += 1
    if ui == len(buttonList): signalScore = True
      
def on_mouse_down(pos):
    global myButtons, playingAnimation, gameCountdown, playerInput
    if not playingAnimation and gameCountdown == 0:
        bcount = 0
        for b in myButtons:
            if b.collidepoint(pos):
                playerInput.append(bcount)
                b.state = True
            bcount += 1
        checkPlayerInput()
   
def on_mouse_up(pos):
    global myButtons, gameStarted, gameCountdown, signalScore, score
    if not playingAnimation and gameCountdown == 0:
        for b in myButtons: b.state = False
    if playButton.collidepoint(pos) and gameStarted == False:
        gameStarted = True
        score = 0
        gameCountdown = LOOPDELAY
    if signalScore:
        score += 1
        gameCountdown = LOOPDELAY
        clearButtons()
        signalScore = False

def clearButtons():
    global myButtons
    for b in myButtons: b.state = False

def playAnimation():
    global playPosition, playingAnimation
    playPosition = 0
    playingAnimation = True

def addButton():
    global buttonList
    buttonList.append(randint(0, 3))
    playAnimation()

pgzrun.go()
