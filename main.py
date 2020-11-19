import pygame, sys
import world

pygame.display.init()
clock = pygame.time.Clock()
Env = world.env()
while True:
    #handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    Env.animation()
    pygame.display.flip()
    clock.tick(60)