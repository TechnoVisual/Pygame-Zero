# gameinput Module

from pygame import joystick, key
from pygame.locals import *

joystick.init()
joystick_count = joystick.get_count()

if(joystick_count > 0):
    joyin = joystick.Joystick(0)
    joyin.init()

def checkInput(p):
    global joyin, joystick_count
    xaxis = yaxis = 0
    if p.status == 0:
        if joystick_count > 0:
            xaxis = joyin.get_axis(0)
            yaxis = joyin.get_axis(1)
        if key.get_pressed()[K_LEFT] or xaxis < -0.8:
            p.angle = 180
            p.movex = -20
        if key.get_pressed()[K_RIGHT] or xaxis > 0.8:
            p.angle = 0
            p.movex = 20
        if key.get_pressed()[K_UP] or yaxis < -0.8:
            p.angle = 90
            p.movey = -20
        if key.get_pressed()[K_DOWN] or yaxis > 0.8:
            p.angle = 270
            p.movey = 20
    if joystick_count > 0:
        jb = joyin.get_button(1)
    else:
        jb = 0
    if p.status == 1:
        if key.get_pressed()[K_RETURN] or jb:
            return 1
    if p.status == 2:
        if key.get_pressed()[K_RETURN] or jb:
            return 1
        
            
    
