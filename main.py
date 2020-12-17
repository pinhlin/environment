import pygame, sys
from world import Kitchen


kitchen = Kitchen() # should be able to configure position of objects as an argument to this
# This was simple plan earlier
# ['pick','object1','back','object1','put','object1','plt_target', 'back', 'none',\	        
# 'pick','object2','back','object2','put', 'object2','object1','back', 'none']
#kitchen.open_drawer('drawer3')
#kitchen.open_drawer('drawer2')
kitchen.open_drawer('drawer1')
kitchen.pick_up('coffee')
kitchen.put('coffee', 'drawer1')
#kitchen.close_drawer('drawer1')
#kitchen.pour('cup', 'coffee')
#kitchen.put('coffee', 100)
#kitchen.fill_water('cup', 'faucet')
#kitchen.put('cup', 'faucet')
#kitchen.pick_up('spoon')
#kitchen.stir('spoon', 'cup')
#kitchen.put('spoon', 30)