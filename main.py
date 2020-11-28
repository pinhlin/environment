import pygame, sys
from world import Kitchen

pygame.display.init()
clock = pygame.time.Clock()
kitchen = Kitchen()
while True:
    #handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    kitchen.run()
    pygame.display.flip()
    clock.tick(60)