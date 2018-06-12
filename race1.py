# PyGame Zero Racing Game
from random import randint

# First set the width and height of the window
WIDTH = 700
HEIGHT = 600

# Load in the car sprite image as an Actor object
car = Actor("racecar")
car.pos = 250, 500 # Set the car screen position

# Some variables to control the track
SPEED = 4
trackCount = 0
trackPosition = 250
trackWidth = 120
trackDirection = False
# The following variables set up the track sprites
trackLeft = []
trackRight = [] 
# Variable to track the status of the game
gameStatus = 0

# Pygame Zero draw function 
def draw():
    global gameStatus
    screen.fill((128, 128, 128))
    if gameStatus == 0:
        car.draw()
        b = 0
        while b < len(trackLeft):
            if car.colliderect(trackLeft[b]) or car.colliderect(trackRight[b]):
                # Red flag time
                gameStatus = 1
            trackLeft[b].draw()
            trackLeft[b].y += SPEED
            trackRight[b].draw()
            trackRight[b].y += SPEED
            b += 1
    if gameStatus == 1:
        # Red Flag
        screen.blit('rflag', (318, 268))
    if gameStatus == 2:
        # Chequered Flag
        screen.blit('cflag', (318, 268))

# Pygame Zero update function
def update():
    global gameStatus , trackCount
    if gameStatus == 0:
        if keyboard.left:
            car.x -= 2
        elif keyboard.right:
            car.x += 2
        updateTrack()
    if trackCount > 200:
        # Chequered flag time
        gameStatus = 2

# Our game functions

# Function to make a new section of track
def makeTrack():
    global trackCount, trackLeft, trackRight, trackPosition, trackWidth
    trackLeft.append(Actor("barrier", pos = (trackPosition-trackWidth,0)))
    trackRight.append(Actor("barrier", pos = (trackPosition+trackWidth,0)))
    trackCount += 1
    
# Function to update where the track blocks appear
def updateTrack():
    global trackCount, trackPosition, trackDirection, trackWidth 
    if trackLeft[len(trackLeft)-1].y > 32:
        if trackDirection == False:
            trackPosition += 16
        if trackDirection == True:
            trackPosition -= 16
            
        if randint(0, 4) == 1:
            trackDirection = not trackDirection
        if trackPosition > 700-trackWidth:
            trackDirection = True
        if trackPosition < trackWidth:
            trackDirection = False
        makeTrack()
                            
# End of functions
                
makeTrack() # Make first block of track

	
	

        
