progress=0
max_progress=100

if earth.norm_velocity() > 5:
    progress += 0.026

progress_box_x, progress_box_y = 350, 200
progress_box_width, progress_box_height = 100, 300
progress_fill_width=(progress/max_progress)*progress_box_width

pygame.draw.rect(screen, (90, 102, 92), (progress_box_x, progress_box_y, progress_box_width, progress_box_height), 2)
pygame.draw.rect(screen, (222, 173, 45), (progress_box_x, progress_box_y, progress_fill_width, progress_box_height))