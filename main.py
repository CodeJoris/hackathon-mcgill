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

# Colors
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)

# Fonts
FONT = pygame.font.Font(None, 12)

# Button properties
button_rect = pygame.rect(10,10,30,30)
button_text = "Add mass"

# Create screen and clock
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()

# Background color
BACKGROUND = (30, 30, 30)

# Create Masses
sun = m.Mass("Sun", 6.957 * 10, 1.989 * 10**30, WIDTH / 2, HEIGHT / 2, (0, 0), (255, 255, 0))
earth = m.Mass("Earth", 2 * 6.378, 5.9722 * 10**27, (WIDTH / 2) + 300, HEIGHT / 2, (0, -1), (0, 0, 255))

trail = []

# Main loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouse_hover = False
        if event.type == pygame.QUIT:
            running = False

        # Mouse button press (start dragging)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if slider_visible and slider_handle_x <= mouse_x <= slider_handle_x + slider_handle_width and slider_y <= mouse_y <= slider_y + slider_handle_height:
                dragging = True
            elif button_rect.collidepoint(event.pos):  # Check if the button was clicked
                slider_visible = not slider_visible  # Toggle slider visibility

        # Mouse button release (stop dragging)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # If dragging, update the slider handle position and value
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        slider_handle_x = max(slider_x, min(mouse_x - slider_handle_width // 2, slider_x + slider_width - slider_handle_width))
        slider_value = (slider_handle_x - slider_x) / (slider_width - slider_handle_width)

    # Detect mouse hover over the button
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        mouse_hover = True


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

    # Draw the button
    button_color = HOVER_COLOR if mouse_hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

    # Render the button text
    text_surface = FONT.render(button_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    # Draw the slider if visible
    if slider_visible:
        # Draw the slider background (the bar)
        pygame.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))

        # Draw the slider handle (the draggable part)
        pygame.draw.rect(screen, (255, 0, 0), (slider_handle_x, slider_y - (slider_handle_height - slider_height) // 2, slider_handle_width, slider_handle_height))

        # Display the slider value
        slider_value_text = FONT.render(f"Value: {slider_value:.2f}", True, TEXT_COLOR)
        screen.blit(slider_value_text, (WIDTH // 2 - slider_value_text.get_width() // 2, slider_y - 50))

    # Update display
    pygame.display.flip()
    clock.tick(100)

pygame.quit()
