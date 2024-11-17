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
FONT = pygame.font.Font(None, 16)

# Button properties
button_rect = pygame.Rect(10, 10, 80, 50)  # x, y, width, height
button_text = "Change Mass"

# Slider properties
slider_x = 100  # Starting X position of the slider
slider_y = 30  # Y position of the slider
slider_width = 300  # Width of the slider bar
slider_height = 10  # Height of the slider bar
slider_handle_width = 20  # Width of the slider handle
slider_handle_height = 20  # Height of the slider handle

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
    return red, 0, blue

# Helper function to reset the slider when you hit something
def initialize_slider():
    global slider_visible, dragging, slider_handle_x, slider_value
    

    slider_value = 0.0
    slider_handle_x = slider_x + slider_value * (slider_width - slider_handle_width)  # Initial handle position

    slider_visible = False  # Controls whether the slider is visible
    dragging = False        # Tracks if the slider handle is being dragged

# Velocity vector helper function
def restart():
    global slider_value, fuel_level, fill_width, lives, progress
    progress=0
    time.sleep(3)
    earth.restart()
    initialize_slider()
    slider_value = 0.0
    fuel_level = 100
    trail.clear()
    trail_colors.clear()
    fill_width = (fuel_level / max_fuel) * box_width
    lives -= 1

# Velocity vector helper function
def velocity_vector():
    position = earth.get_position()
    velocity = earth.get_velocity() 

    # Scale the velocity vector for visibility
    scale = 50  # Adjust as needed
    scaled_velocity = velocity * scale

    end_position = position + scaled_velocity

    # Draw the velocity vector
    pygame.draw.line(screen, (250, 0, 0), position, end_position, width=2)  # Red line for velocity
    pygame.draw.circle(screen, (0, 255, 0), position.astype(int), 4)  # Small green circle at Earth's position


# Create screen and clock
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()

#Image fo the sun
sun_image = pygame.image.load('sun.png').convert_alpha()
sun_size = (70,70)
sun_image = pygame.transform.scale(sun_image,sun_size)
sun_image.set_colorkey((255,255,255))

#Image of the Satellite
sat_image = pygame.image.load('satellite.jpg').convert_alpha()
sat_size = (50,50)
sat_image = pygame.transform.scale(sat_image,sat_size)
sat_image.set_colorkey((255,255,255))

#IMage heart
lives_image = pygame.image.load('heart.jpg').convert_alpha()
lives_size = (50,50)
lives_image = pygame.transform.scale(lives_image,lives_size)
lives_image.set_colorkey((255,255,255))


# Win lose screens
font = pygame.font.Font(None, 36)
lose_text_surface = font.render('You Lose', True, (255,0,0))
lose_text = lose_text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))

win_text_surface = font.render('You WIN', True, (255,0,0))
win_text = lose_text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 -100))




# Create Masses
sun = m.Mass("Sun", 25, 1.989 * 10**30, WIDTH / 2, HEIGHT / 2, (0, 0), (255, 255, 0))
earth = m.Mass("Earth", 25, 5.9722 * 10**27, (WIDTH / 2) + 300, HEIGHT / 2, (0, -1), (0, 0, 255))

trail = []
trail_colors = []
initial_norm = earth.norm_velocity()
red_shift = 0
blue_shift = 255
TRAIL_COLOR = (red_shift,0,blue_shift)

lives = 3
min_speed = 0
max_speed = 5



# Fuel level rectangles
fuel_level = 100
max_fuel = 100
box_x, box_y = 10, HEIGHT-50
box_width, box_height = 300, 40
fill_width=(fuel_level/max_fuel)*box_width

# Progress bar
progress=0
max_progress=100
fuel_box_x, fuel_box_y = WIDTH//2, HEIGHT-50
fuel_box_width, fuel_box_height = 300, 40
fuel_fill_width=(progress/max_progress)*fuel_box_width

#fuel text
font = pygame.font.Font(None, 36)
fuel_tag_text = f"Fuel Levels : {int(fuel_level)} / {max_fuel}"
fuel_text_surface = font.render(fuel_tag_text, True, (255,0,0))
fuel_text = fuel_text_surface.get_rect(center=(fuel_box_x + fuel_box_width // 2, fuel_box_y - 20))  # Position above the box

#progress text
font = pygame.font.Font(None, 36)
progress_tag_text = f"Progress : {int(progress)} / {max_progress}"
progress_text_surface = font.render(progress_tag_text, True, (255,0,0))
progress_text = progress_text_surface.get_rect(center=(box_x + box_width // 2, box_y - 20))  # Position above the box



# Add masses to group
all_sprites = pygame.sprite.Group()
all_sprites.add(sun, earth)



    
# Variables
running = True
win = False
lose = False

# Main loop

initialize_slider()
while running:
    
    if not win and not lose:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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



        # Update physics
        earth.apply_acceleration_due_to(sun)
        earth.update()

        # Update trail
        speed = earth.norm_velocity()
        earth_pos = earth.pygame_position()
        trail_colors.append(speed_to_color(speed, min_speed, max_speed))
        trail.append(tuple(earth_pos))

        # Update suns mass based on the slider
        sun_mass = 3*(slider_value*sun.originalData[1]) + 1*(sun.originalData[1]) # y = 0.2x + 0.9 (scaled by mass of the sun)
        sun.set_mass(sun_mass)

        # Win condition
        if progress >= 100:
            win = True

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        #draw velocity vector
        velocity_vector()

        # Draw trail
        if len(trail) > 1:
            for i in range(1, len(trail)):
                pygame.draw.line(screen, trail_colors[i], trail[i - 1], trail[i], 2)

        # Draw sun and earth
        screen.blit(sun_image,(WIDTH//2 - sun_size[0]//2, HEIGHT//2 - sun_size[1]//2))
        screen.blit(sat_image,(earth.get_position()[0] - sat_size[0]//2, earth.get_position()[1]  - sat_size[1]//2))

        # Draw the button
        button_color = BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

        # Render the button text
        text_surface = FONT.render(button_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        
        # check for collision with the sun
        if (pygame.sprite.collide_circle(earth, sun)):
            if (lives > 1):
                restart()
            else:
                lose = True

        # check for collision with the border
        for sprite in all_sprites:
            if (sprite.rect.x < 0 or sprite.rect.right > WIDTH or sprite.rect.y < 0 or sprite.rect.bottom > HEIGHT):
                if (lives > 1):
                    restart()
                else:
                    lose = True

        # velocity earth
        if earth.norm_velocity() > 3:
            progress += 0.26
        fuel_fill_width=(progress/max_progress)*fuel_box_width

        all_sprites.update()

        #draw fuel text
        fuel_text = f"Fuel Levels : {int(fuel_level)} / {max_fuel}"
        fuel_text_surface = font.render(fuel_text, True, (255,0,0))
        fuel_text_pos = (box_x, box_y - 40)
        screen.blit(fuel_text_surface, fuel_text_pos)

        #Draw hearts
        for i in range(lives):
            screen.blit(lives_image,(940-60*i,20))

        #draw progress text
        progress_text = f"Progress Level : {int(progress)} / {max_progress}"
        progress_text_surface = font.render(progress_text, True, (255,255,0))
        progress_text_pos = (fuel_box_x, fuel_box_y - 40)
        screen.blit(progress_text_surface, progress_text_pos)

        #draw fuel rectable
        pygame.draw.rect(screen, (90, 102, 92), (fuel_box_x, fuel_box_y, fuel_box_width, fuel_box_height), 2)
        pygame.draw.rect(screen, (222, 173, 45), (fuel_box_x, fuel_box_y, fuel_fill_width, fuel_box_height))
            
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

    elif win:
        screen.blit(win_text_surface,win_text)
    
    elif lose:
        screen.blit(lose_text_surface,lose_text)

    # Update display
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
