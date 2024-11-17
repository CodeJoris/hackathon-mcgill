progress=0
max=100

if earth.norm_velocity() > 5:
    progress += 0.026

box_x, box_y = 350, 200
box_width, box_height = 100, 300
fill_width=(progress/max)*box_width

pygame.draw.rect(screen, (90, 102, 92), (box_x, box_y, box_width, box_height), 2)
pygame.draw.rect(screen, (222, 173, 45), (box_x, box_y, fill_width, box_height))