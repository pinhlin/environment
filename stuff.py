import pygame, sys, time

class block(object):
    def __init__(self, color, width, height, init_x, init_y):
        #object
        self.color = color
        self.object_width = width #26
        self.object_height = height #50
        self.object_x = init_x #100 #initail position x
        self.object_y = init_y #330 #initioal position y
        self.object_speed_x = 0 #initialize the speed be 0
        self.object_speed_y = 0 #initailize the speed be 0
        self.object = pygame.Rect(self.object_x, self.object_y, self.object_width, self.object_height)

#Platform class is particular for this test, can be deleted for future purpose
class platform(object):
    def __init__(self, color, width, height, init_x, init_y):
        #platform_org
        self.color = color
        self.platform_width = width#50
        self.platform_height = height#50y
        self.platform = pygame.Rect(init_x, init_y, self.platform_width, self.platform_height)
