import pygame, sys, time
import numpy as np
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TABLE_HEIGHT = SCREEN_HEIGHT-50
class spoon(object):
    def __init__(self, color, width, height, init_x, init_y, std = 2):
        self.color = color
        self.object_width = width 
        self.object_height = height 
        self.object_x = init_x #initail position x
        self.object_y = init_y #initioal position y
        self.object_speed_x = 0 #initialize the speed be 0
        self.object_speed_y = 0 #initailize the speed be 0
        self.shaft = pygame.Rect(self.object_x, self.object_y, self.object_width, self.object_height)
        self.head = pygame.Rect(self.object_x-5, self.object_y+height, self.object_width+10, 10)
        self.object = pygame.Rect.union(self.shaft, self.head)
        self.hold =self.shaft
    def update(self):
        self.object.x += self.object_speed_x
        self.object.y += self.object_speed_y
        self.shaft.x += self.object_speed_x
        self.shaft.y += self.object_speed_y
        self.head.x += self.object_speed_x
        self.head.y += self.object_speed_y

class cup(object):
    def __init__(self, color, width, height, init_x, std = 2):
        #object
        rim_width = 3
        self.color = color
        self.object_width = width + 2*rim_width
        self.object_height = height 
        self.object_x = init_x #initail position x
        self.object_y =  TABLE_HEIGHT - height#initioal position y
        self.object_speed_x = 0 #initialize the speed be 0
        self.object_speed_y = 0 #initailize the speed be 0
        self.left = pygame.Rect(self.object_x, self.object_y, rim_width, self.object_height)
        self.right = pygame.Rect(self.object_x+rim_width+width, self.object_y, rim_width, self.object_height)
        self.bottom = pygame.Rect(self.object_x+rim_width, TABLE_HEIGHT-rim_width, width, rim_width)
        self.object = self.bottom.unionall([self.left, self.right])
        self.hold = self.object
        self.sigma = std #std of the normal distribution, for uncertainty

    def update(self):
        self.object.x += self.object_speed_x
        self.object.y += self.object_speed_y
        self.left.x += self.object_speed_x
        self.left.y += self.object_speed_y
        self.right.x += self.object_speed_x
        self.right.y += self.object_speed_y
        self.bottom.x += self.object_speed_x
        self.bottom.y += self.object_speed_y

    def getpos(self): # return the normal distribution of the possible position
        pos = {}
        pos['x'] = np.random.normal(self.object.x, self.sigma, 1000)
        pos['y'] = np.random.normal(self.object.y, self.sigma, 1000)
        return pos



"""
class block(object):
    def __init__(self, color, width, height, init_x, init_y, std = 2):
        #object
        self.color = color
        self.object_width = width 
        self.object_height = height 
        self.object_x = init_x #initail position x
        self.object_y = init_y #initioal position y
        self.object_speed_x = 0 #initialize the speed be 0
        self.object_speed_y = 0 #initailize the speed be 0
        self.object = pygame.Rect(self.object_x, self.object_y, self.object_width, self.object_height)
        self.sigma = std #std of the normal distribution, for uncertainty

    def update(self):
        self.object.x += self.object_speed_x
        self.object.y += self.object_speed_y

    def getpos(self): # return the normal distribution of the possible position
        pos = {}
        pos['x'] = np.random.normal(self.object.x, self.sigma, 1000)
        pos['y'] = np.random.normal(self.object.y, self.sigma, 1000)
        return pos

#Platform class is particular for this test, can be deleted for future purpose
class platform(object):
    def __init__(self, color, width, height, init_x, init_y):
        #platform_org
        self.color = color
        self.object_width = width#50
        self.object_height = height#50y
        self.object = pygame.Rect(init_x, init_y, self.object_width, self.object_height)

class freefall(object):
    def __init__(self, color, width, height, init_x, init_y):
        self.color = color
        self.object_width = width 
        self.object_height = height 
        self.object_x = init_x #initail position x
        self.object_y = init_y #initioal position y
        self.object_speed_x = 0 #initialize the speed be 0
        self.object_speed_y = 0 #initailize the speed be 0
        self.object_acc_y = 0.98 #initailize the speed be 0
        self.object = pygame.Rect(self.object_x, self.object_y, self.object_width, self.object_height)
    
    def update(self):
        self.object.x += self.object_speed_x
        self.object.y += self.object_speed_y

    def _check_contact(self, obj_list):
        for obj in obj_list:
            if self.object.colliderect(obj):
                 self.object_speed_y = 0
                 break
"""