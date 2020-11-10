import pygame, sys
import test

pygame.display.init()
clock = pygame.time.Clock()
Env = test.env()
while True:
    #handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    Env.objAnimation()
    pygame.display.flip()
    clock.tick(60)