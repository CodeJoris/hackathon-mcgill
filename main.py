### Main Code ###
import numpy as np
import sys, pygame, time, os
from pygame.locals import *
from random import randint, choice


import Mass as m
import Vector as v
from math import cos,sin 
# >>>>>>> cb61859c766c4646f5cde64f6ff4895c0f046f99
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,30)
#Configuration
DIMENSIONS = WIDTH, HEIGHT =(1000,1000)
CENTER=(DIMENSIONS[0]/2,DIMENSIONS[1]/2)

VITESSE=10

screen = pygame.display.set_mode(DIMENSIONS)
rafraichissement = pygame.time.Clock()
G=6.67*10**-11
BACKGROUND = (0,0,0)
pygame.init()
### Definition of our two masses using class Mass ###
sun = m.Mass("Sun",6.957*10,1.989*10**30,WIDTH/2,HEIGHT/2,0,(255,255,0))
earth = m.Mass("Earth",2*6.378,5.9722*10**24,(WIDTH/2)+300,HEIGHT/2,np.array([0,1]),(0,0,255))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(BACKGROUND)

    # Draw a sun
    pygame.draw.circle(screen, sun.color, sun.pygame_position(), sun.radius)
    pygame.draw.circle(screen, earth.color, earth.pygame_position(), earth.radius)

   # Update the display
    pygame.display.flip()
    rafraichissement.tick(60)

# Quit Pygame
pygame.quit()


#Fonction qui prend en input un vector et qui output un vector
def velocity_update(velocity,acceleration,time_interval):
    velocity = velocity+acceleration*time_interval
    return velocity