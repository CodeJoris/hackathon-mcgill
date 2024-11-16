### Main Code ###
import numpy as np
import sys, pygame, time, os
from pygame.locals import *
from random import randint, choice

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,30)


VITESSE=10

screen = pygame.display.set_mode(DIMENSIONS)
rafraichissement = pygame.time.Clock()

BACKGROUND = (0,0,0)

### Definition of our two masses using class Mass ###
sun = Mass("Sun",6.957*10**8,1.989*10**30,WIDTH/2,HEIGHT/2,0,"Yellow")
earth = Mass("Earth",6.378*10**6,5.9722*10**24,(WIDTH/2)+300,HEIGHT/2,np.array([0,1]),"Blue")

G=6.67*10**-11
acceleration = G



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(BACKGROUND)

    # Draw a sun
    pygame.draw.circle(screen, sun.color, sun.pos, sun.radius)
    pygame.draw.circle(screen, earth.color, earth.pos, earth.radius)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()


#Fonction qui prend en input un vector et qui output un vector
def velocity_update(velocity,acceleration,time_interval):
    velocity = velocity+acceleration*time_interval
    return velocity