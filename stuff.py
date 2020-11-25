import pygame, sys, time
import numpy as np
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
