def lives_hearts(lives):
    lives_image = pygame.image.load('sun.png').convert_alpha()
    lives_size = (50,50)
    lives_image = pygame.transform.scale(lives_image,lives_size)
    lives_image.set_colorkey((255,255,255))
    for i in range(lives):
        screen.blit(lives_image,(940-60*i,20))