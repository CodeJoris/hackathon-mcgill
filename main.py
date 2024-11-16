### Main Code ###
import numpy as np
import sys, pygame, time, os
from pygame.locals import *
from random import randint, choice


import Mass as m
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
sun = m.Mass("Sun",6.957*10, 1.989*10**30,WIDTH/2,HEIGHT/2,(0,0),(255,255,0))
earth = m.Mass("Earth",1.4*6.378, 5.9722*10**24,(WIDTH/2)+300,HEIGHT/2,(0,-1),(0,0,255))
moon = m.Mass("Moon",0.7*6.378, 5.9722*10**22,(WIDTH/2)+305,HEIGHT/2,(0,-1.1),(255,0,0))


trail = []
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    
    earth_pos=earth.pygame_position()

    
    # Add current position to the trail
    trail.append(tuple(earth_pos))  # Store position as a tuple
    if len(trail) > 1000:  # Limit trail length for performance
        trail.pop(0)


    screen.fill(BACKGROUND)

    # Draw the trail
    if len(trail) > 1:
        pygame.draw.lines(screen, (0, 255, 0), False, trail, 2)


    # Draw a sun
    earth.update_position()
    moon.update_position()
    earth.apply_acceleration_due_to(sun)
    moon.apply_acceleration_due_to(earth)
    
  
    

    pygame.draw.circle(screen, moon.color, moon.pygame_position(), moon.radius)
    pygame.draw.circle(screen, sun.color, sun.pygame_position(), sun.radius)
    pygame.draw.circle(screen, earth.color, earth_pos, earth.radius)


   # Update the display
    pygame.display.flip()
    rafraichissement.tick(60)

# Quit Pygame
pygame.quit()


#Fonction qui prend en input un vector et qui output un vector
def velocity_update(velocity,acceleration,time_interval):
    velocity = velocity+acceleration*time_interval
    return velocity