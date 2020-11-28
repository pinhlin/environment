import pygame, sys
from world import Kitchen


kitchen = Kitchen()
# This was simple plan earlier
# ['pick','object1','back','object1','put','object1','plt_target', 'back', 'none',\	        
# 'pick','object2','back','object2','put', 'object2','object1','back', 'none']

kitchen.pick_up('object1')
kitchen.put('object1', 'plt_target')
kitchen.pick_up('object2')
kitchen.put('object2', 'object1')
kitchen.run()

# pygame.display.init()
# clock = pygame.time.Clock()
# kitchen = Kitchen()
# while True:
#     #handling input
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     kitchen.run()
#     pygame.display.flip()
#     clock.tick(60)