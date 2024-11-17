progress=0
max_progress=100
font = pygame.font.Font(None, 36)
fuel_tag_text = f"Progress : {int(progress)} / {max_progress}"
fuel_text_surface = font.render(fuel_tag_text, True, (255,0,0))
fuel_text_rect = fuel_text_surface.get_rect(center=(progress_box_x + progress_box_width // 2, progress_box_y - 20))  # Position above the box
screen.blit(fuel_text_surface, fuel_text_rect)

#####
fuel_level=100
max_fuel=100
tag_text = f"Fuel Levels : {int(fuel_level)} / {max_fuel}"
text_surface = font.render(tag_text, True, (255,0,0))
text_rect = text_surface.get_rect(center=(box_x + box_width // 2, box_y - 20))  # Position above the box
screen.blit(text_surface, text_rect)


#draw fuel text
    fuel_text = f"Fuel Levels : {int(fuel_level)} / {max_fuel}"
    fuel_text_surface = font.render(fuel_text, True, (255,0,0))
    fuel_text_pos = (box_x + box_width // 2, box_y - 20)
    screen.blit(fuel_text_surface, fuel_text_pos)

    #draw progress text
    progress_text = f"Progress Level : {int(progress)} / {max_progress}"
    progress_text_surface = font.render(progress_text, True, (255,0,0))
    progress_text_pos = (fuel_box_x + fuel_box_width // 2, fuel_box_y - 20)
    screen.blit(progress_text_surface, progress_text_pos)
