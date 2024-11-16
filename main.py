import numpy as np
import sys, pygame, os
from pygame.locals import *
from math import cos, sin

import Mass as m

# Initialize Pygame
pygame.init()

# Screen dimensions
DIMENSIONS = WIDTH, HEIGHT = (1000, 800)
CENTER = (WIDTH / 2, HEIGHT / 2)

# Slider properties
slider_x = 100
slider_y = 900  # Position it below the simulation area
slider_width = 600
slider_height = 10
slider_handle_width = 20
slider_handle_height = 20



slider_value = 0.5  # Initial slider value
slider_handle_x = slider_x + slider_value * (slider_width - slider_handle_width)

# Button properties
button_rect = pygame.rect(10,10,30,30)
button_text = "Add mass"

# Create screen and clock
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()

# Background color
BACKGROUND = (30, 30, 30)

# Create Masses
sun = m.Mass("Sun", 6.957 * 10, 1.989 * 10**30, WIDTH / 2, HEIGHT / 2, (1, 0), (255, 255, 0))
earth = m.Mass("Earth", 0.7 * 6.378, 5.9722 * 10**27, (WIDTH / 2) + 300, HEIGHT / 2, (0, -0.5), (0, 0, 255))

trail = []

# Main loop
dragging = False 
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



        # Handle mouse input for slider
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (slider_handle_x <= mouse_x <= slider_handle_x + slider_handle_width and
                slider_y <= mouse_y <= slider_y + slider_handle_height):
                dragging = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Check if the button was clicked
                    print("Button clicked!")

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # Update slider position if dragging
    if dragging:
        mouse_x, _ = pygame.mouse.get_pos()
        slider_handle_x = max(slider_x, min(mouse_x - slider_handle_width // 2, slider_x + slider_width - slider_handle_width))
        slider_value = (slider_handle_x - slider_x) / (slider_width - slider_handle_width)

    # Update physics
    earth.apply_acceleration_due_to(sun)
    earth.update_position()

    # Update trail
    earth_pos = earth.pygame_position()
    trail.append(tuple(earth_pos))
    if len(trail) > 1000:
        trail.pop(0)

    # Clear screen
    screen.fill(BACKGROUND)

    # Draw trail
    if len(trail) > 1:
        pygame.draw.lines(screen, (0, 255, 0), False, trail, 2)

    # Draw sun and earth
    pygame.draw.circle(screen, sun.color, sun.pygame_position(), sun.radius)
    pygame.draw.circle(screen, earth.color, earth.pygame_position(), earth.radius)

    # Draw the slider background (the bar)
    pygame.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))

    # Draw the slider handle (the draggable part)
    pygame.draw.rect(screen, (255, 0, 0),
                     (slider_handle_x, slider_y - (slider_handle_height - slider_height) // 2, slider_handle_width,
                      slider_handle_height))

    # Draw slider value (optional)
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Value: {slider_value:.2f}", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, slider_y - 50))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
