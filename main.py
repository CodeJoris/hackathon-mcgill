import time

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
button_rect = pygame.Rect(10, 10, 50, 50)  # x, y, width, height
button_text = "Add Mass"

# Slider properties
slider_x = 20  # Starting X position of the slider
slider_y = 15  # Y position of the slider
slider_width = 600  # Width of the slider bar
slider_height = 10  # Height of the slider bar
slider_handle_width = 20  # Width of the slider handle
slider_handle_height = 20  # Height of the slider handle

# Initial slider value (percentage)
slider_value = 0.5  # Value between 0 and 1 (50%)
slider_handle_x = slider_x + slider_value * (slider_width - slider_handle_width)  # Initial handle position

# Variables
running = True
slider_visible = False  # Controls whether the slider is visible
dragging = False        # Tracks if the slider handle is being dragged

# Create screen and clock
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()

#Image
sun_image = pygame.image.load('sun.png').convert_alpha()
sun_size = (70,70)
sun_image = pygame.transform.scale(sun_image,sun_size)
sun_image.set_colorkey((255,255,255))

sat_image = pygame.image.load('satellite.jpg').convert_alpha()
sat_size = (50,50)
sat_image = pygame.transform.scale(sat_image,sat_size)
sat_image.set_colorkey((255,255,255))


# Background color
BACKGROUND = (30, 30, 30)

# Create Masses
sun = m.Mass("Sun", 25, 1.989 * 10**30, WIDTH / 2, HEIGHT / 2, (0, 0), (255, 255, 0))
earth = m.Mass("Earth", 25, 5.9722 * 10**27, (WIDTH / 2) + 300, HEIGHT / 2, (0, -1), (0, 0, 255))

trail = []
trail_colors = []
initial_norm = earth.norm_velocity()
red_shift = 0
blue_shift = 255
TRAIL_COLOR = (red_shift,0,blue_shift)


min_speed = 0
max_speed = 5

# Helper function to map speed to color
def speed_to_color(speed, min_speed, max_speed):
    """
    Maps the speed to a color gradient (blue to red).
    """
    # Normalize speed to a 0-1 range
    normalized_speed = max(0, min(1, (speed - min_speed) / (max_speed - min_speed)))
    # Interpolate between blue (slow) and red (fast)
    red = int(255 * normalized_speed)
    blue = int(255 * (1 - normalized_speed))
    return (red, 0, blue)

# Fuel level rectangles
fuel_level = 100
max_fuel = 100
box_x, box_y = 10, HEIGHT-50
box_width, box_height = 300, 40
fill_width=(fuel_level/max_fuel)*box_width

# Progress bar
progress=0
max_progress=100
progress_box_x, progress_box_y = WIDTH//2, HEIGHT-50
progress_box_width, progress_box_height = 300, 40
progress_fill_width=(progress/max_progress)*progress_box_width



# Add masses to group
all_sprites = pygame.sprite.Group()
all_sprites.add(sun, earth)

# Main loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouse_hover = False

        if event.type == pygame.KEYDOWN:
            
            fill_width=(fuel_level/max_fuel)*box_width
            if fuel_level>0:
                if event.key == pygame.K_UP:  # Up arrow key
                    fuel_level-=1
                    earth.apply_custom_acceleration(np.array([0,-0.5]))
                elif event.key == pygame.K_DOWN:  # Down arrow key
                    fuel_level-=1
                    earth.apply_custom_acceleration(np.array([0,0.5]))
                elif event.key == pygame.K_LEFT:  # Left arrow key
                    fuel_level-=1
                    earth.apply_custom_acceleration(np.array([-0.5,0]))
                elif event.key == pygame.K_RIGHT:  # Right arrow key
                    fuel_level-=1
                    earth.apply_custom_acceleration(np.array([0.5,0]))

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
    earth.update()

    # Update trail
    speed = earth.norm_velocity()
    earth_pos = earth.pygame_position()
    trail_colors.append(speed_to_color(speed, min_speed, max_speed))
    trail.append(tuple(earth_pos))
    #if len(trail) > 1000:
        #trail.pop(0)

    # Update suns mass based on the slider
    sun_mass = 0.01*(slider_value*sun.get_mass()) + 0.995*(sun.get_mass()) # y = 0.2x + 0.9 (scaled by mass of the sun)
    sun.set_mass(sun_mass)

    # Clear screen
    screen.fill(BACKGROUND)

    # Draw trail
    if len(trail) > 1:
        for i in range(1, len(trail)):
            pygame.draw.line(screen, trail_colors[i], trail[i - 1], trail[i], 2)

    # Draw sun and earth
    screen.blit(sun_image,(WIDTH//2 - sun_size[0]//2, HEIGHT//2 - sun_size[1]//2))
    screen.blit(sat_image,(earth.get_position()[0] - sat_size[0]//2, earth.get_position()[1]  - sat_size[1]//2))

    # Draw the button
    button_color = HOVER_COLOR if mouse_hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

    # Render the button text
    text_surface = FONT.render(button_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    if (pygame.sprite.collide_circle(earth, sun)):
        time.sleep(3)
        earth.restart()
        slider_value = 0.5
        fuel_level = 100
        trail.clear()
        trail_colors.clear()

        fill_width = (fuel_level / max_fuel) * box_width

    for sprite in all_sprites:
        if (sprite.rect.x < 0 or sprite.rect.right > WIDTH or sprite.rect.y < 0 or sprite.rect.bottom > HEIGHT):
            time.sleep(3)
            earth.restart()
            slider_value = 0.5
            fuel_level = 100
            fill_width = (fuel_level / max_fuel) * box_width
            trail.clear()
            trail_colors.clear()
            break

    # velocity earth
    if earth.norm_velocity() > 1.5:
        progress += 0.026
    progress_fill_width=(progress/max_progress)*progress_box_width

    all_sprites.update()

    #draw progress box
    pygame.draw.rect(screen, (90, 102, 92), (progress_box_x, progress_box_y, progress_box_width, progress_box_height), 2)
    pygame.draw.rect(screen, (222, 173, 45), (progress_box_x, progress_box_y, progress_fill_width, progress_box_height))
        
    #draw rectangles fuel box
    pygame.draw.rect(screen, (200,200,200), (box_x, box_y, box_width, box_height), 2)
    pygame.draw.rect(screen, (215,43,43), (box_x, box_y, fill_width, box_height))

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
    clock.tick(60)

pygame.quit()
