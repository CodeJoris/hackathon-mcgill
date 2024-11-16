fuel_level=100
max_fuel=100
if event.type == pygame.KEYDOWN:
    fuel_level-=0.01
    if event.key == pygame.K_UP:  # Up arrow key
        earth.apply_custom_acceleration(np.array([0,-0.5]))
    elif event.key == pygame.K_DOWN:  # Down arrow key
        earth.apply_custom_acceleration(np.array([0,0.5]))
    elif event.key == pygame.K_LEFT:  # Left arrow key
        earth.apply_custom_acceleration(np.array([-0.5,0]))
    elif event.key == pygame.K_RIGHT:  # Right arrow key
        earth.apply_custom_acceleration(np.array([0.5,0]))

box_x, box_y = 350, 200
box_width, box_height = 100, 300
fill_width=(fuel_level/max_fuel)*box_width

pygame.draw.rect(screen, (200,200,200), (box_x, box_y, box_width, box_height), 2)
pygame.draw.rect(screen, (215,43,43), (box_x, box_y, fill_width, box_height), 2)