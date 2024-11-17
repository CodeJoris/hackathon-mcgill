progress=0
max_progress=100
font = pygame.font.Font(None, 36)
tag_text = f"Progress : {int(progress)} / {max_progress}"
text_surface = font.render(tag_text, True, (255,0,0))
text_rect = text_surface.get_rect(center=(progress_box_x + progress_box_width // 2, progress_box_y - 20))  # Position above the box
screen.blit(text_surface, text_rect)

#####
fuel_level=100
max_fuel=100
tag_text = f"Fuel Levels : {int(fuel_level)} / {max_fuel}"
text_surface = font.render(tag_text, True, (255,0,0))
text_rect = text_surface.get_rect(center=(box_x + box_width // 2, box_y - 20))  # Position above the box
screen.blit(text_surface, text_rect)