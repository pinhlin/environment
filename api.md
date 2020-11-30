Kitchen for Progress 2D API
===========
The Kitchen for Progress 2D API is a simple API meant for an agent to interact with a PyGame simulation of a Kitchen.  
For now, the simulation contains:  
+ A gripper (agent)  
+ A bowl  
+ A cup  
+ A spoon  
+ Three drawers  

# Usage
```
import kitchen

# Create a kitchen object
my_kitchen = kitchen()

# Gripper moves to a bowl and picks it up
my_kitchen.pick('bowl')

# Gripper carries bowl to the sink and fills it with water
my_kitchen.fill('bowl')

# Gripper puts bowl on tray
my_kitchen.put_on('bowl', 'tray')

...
```
# Methods
TBD