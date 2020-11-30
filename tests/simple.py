from kitchen_progress import *

# Create a kitchen object
my_kitchen = Kitchen()

# Gripper moves to a bowl and picks it up
my_kitchen.pick('bowl')

# Gripper carries bowl to the sink and fills it with water
my_kitchen.fill('bowl')

# Gripper puts bowl on tray
my_kitchen.put_on('bowl', 'tray')