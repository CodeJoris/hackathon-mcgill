### Main Code ###
import numpy as np
import sys, pygame, time, os
from pygame.locals import *
from random import randint, choice


import Mass as m
from math import cos,sin 

# Slider properties
slider_x = 100  # Starting X position of the slider
slider_y = 300  # Y position of the slider
slider_width = 600  # Width of the slider bar
slider_height = 10  # Height of the slider bar
slider_handle_width = 20  # Width of the slider handle
slider_handle_height = 20  # Height of the slider handle

# >>>>>>> cb61859c766c4646f5cde64f6ff4895c0f046f99
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,30)
#Configuration
DIMENSIONS = WIDTH, HEIGHT =(1000,1000)
CENTER=(DIMENSIONS[0]/2,DIMENSIONS[1]/2)

VITESSE=10

screen = pygame.display.set_mode(DIMENSIONS)
rafraichissement = pygame.time.Clock()

BACKGROUND = (100,100,100)
pygame.init()
### Definition of our two masses using class Mass ###
sun = m.Mass("Sun",6.957*10, 1.989*10**30,WIDTH/2,HEIGHT/2,(0,0),(255,255,0))
earth = m.Mass("Earth",0.7*6.378, 5.9722*10**27,(WIDTH/2)+300,HEIGHT/2,(0,-1),(0,0,255))
moon = m.Mass("Moon",0.7*6.378, 5.9722*10**22,(WIDTH/2)+305,HEIGHT/2,(0,-0.6),(255,0,0))

# Initial slider value (percentage)
slider_value = 0.5  # Value between 0 and 1 (50%)
slider_handle_x = slider_x + slider_value * (WIDTH - slider_handle_width)  # Calculate the initial handle position

dragging = False

trail = []
running = True
slider=True
while running:
    if slider:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse button press (start dragging)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (slider_handle_x <= mouse_x <= slider_handle_x + slider_handle_width and
                    slider_y <= mouse_y <= slider_y + slider_handle_height):
                    dragging = True

            # Mouse button release (stop dragging)
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

        # If dragging, update the handle position based on mouse X position
        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Make sure the handle stays within the slider bounds
            slider_handle_x = max(slider_x, min(mouse_x - slider_handle_width // 2, slider_x + slider_width - slider_handle_width))

            # Update the slider value
            slider_value = (slider_handle_x - slider_x) / (slider_width - slider_handle_width)

        # Clear the screen
        screen.fill((30, 30, 30))  # Dark background color

        # Draw the slider background (the bar)
        pygame.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))

        # Draw the slider handle (the draggable part)
        pygame.draw.rect(screen, (255, 0, 0), (slider_handle_x, slider_y - (slider_handle_height - slider_height) // 2, slider_handle_width, slider_handle_height))

        # Draw the slider value (optional)
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Value: {slider_value:.2f}", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))
        # Fill the screen with white
    
    if not slider:
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
