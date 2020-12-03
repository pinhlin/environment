import pygame, sys
from world import Kitchen


kitchen = Kitchen()
# This was simple plan earlier
# ['pick','object1','back','object1','put','object1','plt_target', 'back', 'none',\	        
# 'pick','object2','back','object2','put', 'object2','object1','back', 'none']
kitchen.open('drawer3')
kitchen.open('drawer2')
kitchen.open('drawer1')
kitchen.pick_up('coffee')
kitchen.pour('cup', 'coffee')
kitchen.put('coffee', 100)
kitchen.fill_water('cup', 250)
kitchen.put('cup', 180)
kitchen.pick_up('spoon')
kitchen.stir('spoon', 'cup')
kitchen.put('spoon', 30)
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