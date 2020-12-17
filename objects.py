import pygame, sys, time
import pygame.freetype
import numpy as np
pygame.freetype.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TABLE_HEIGHT = SCREEN_HEIGHT-50
FONT = pygame.freetype.Font('fonts/OpenSans-Light.ttf', 12)
class Spoon(object):
    def __init__(self, color, width, height, init_x, init_y, addText = False, std = 2):
        self.addText = addText
        self.text = None
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
        self.object_speed_x = 0
        self.object_speed_y = 0

class Cup(object):
    def __init__(self, color, width, height, init_x, bottom, addText = False, std = 2):
        #object
        rim_width = 3
        self.addText = addText
        self.text = None
        self.color = color
        self.object_width = width + 2*rim_width
        self.object_height = height 
        self.object_x = init_x #initail position x
        self.object_y =  bottom - height#initioal position y
        self.object_speed_x = 0 #initialize the speed be 0
        self.object_speed_y = 0 #initailize the speed be 0
        self.left = pygame.Rect(self.object_x, self.object_y, rim_width, self.object_height)
        self.right = pygame.Rect(self.object_x+rim_width+width, self.object_y, rim_width, self.object_height)
        self.bottom = pygame.Rect(self.object_x+rim_width, bottom-rim_width, width, rim_width)
        self.coffee = pygame.Rect(self.object_x+rim_width, self.object_y+(height/2), width, height/2)
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
        self.coffee.x += self.object_speed_x
        self.coffee.y += self.object_speed_y
        self.object_speed_x = 0
        self.object_speed_y = 0

    def getpos(self): # return the normal distribution of the possible position
        pos = {}
        pos['x'] = np.random.normal(self.object.x, self.sigma, 1000)
        pos['y'] = np.random.normal(self.object.y, self.sigma, 1000)
        return pos

class Drawer(object):
    def __init__(self, color, width, height, init_x, init_y, contain = None, addText = False, std = 2):
        #object
        self.addText = addText
        self.contain = contain
        self.text_string = None
        self.text = None
        self.color = color
        self.object_width = width 
        self.object_height = height 
        self.object_x = init_x #initail position x
        self.object_y = init_y #initioal position y
        self.object_speed_x = 0 #initialize the speed be 0
        self.object_speed_y = 0 #initailize the speed be 0
        self.object = pygame.Rect(self.object_x, self.object_y, self.object_width, self.object_height)
        self.bottom = pygame.Rect(self.object_x, self.object_y+self.object_height, self.object_width, 0)
        self.hold = self.object
        self.sigma = std #std of the normal distribution, for uncertainty

    def update(self):
        self.object.x += self.object_speed_x
        self.object.y += self.object_speed_y
        self.bottom.x += self.object_speed_x
        self.bottom.y += self.object_speed_y
        if self.addText:
            self.text = self.addText2Block(self.text_string)
        if self.contain != None:
            self.contain.object_speed_x = self.object_speed_x
            self.contain.object_speed_y = self.object_speed_y
            self.contain.update()
        self.object_speed_x = 0
        self.object_speed_y = 0

    def getpos(self): # return the normal distribution of the possible position
        pos = {}
        pos['x'] = np.random.normal(self.object.x, self.sigma, 1000)
        pos['y'] = np.random.normal(self.object.y, self.sigma, 1000)
        return pos
    
    def addText2Block(self, text):
        if self.text_string == None: 
            self.text_string = text
        self.text = FONT.render(self.text_string, 'Red'), (self.object.x, self.object.y+self.object_height/2)
        return self.text

class Block(object):
    def __init__(self, color, width, height, init_x, init_y, addText = False, std = 2):
        #object
        self.addText = addText
        self.text_string = None
        self.text = None
        self.color = color
        self.object_width = width 
        self.object_height = height 
        self.object_x = init_x #initail position x
        self.object_y = init_y #initioal position y
        self.object_speed_x = 0 #initialize the speed be 0
        self.object_speed_y = 0 #initailize the speed be 0
        self.object = pygame.Rect(self.object_x, self.object_y, self.object_width, self.object_height)
        self.hold = self.object
        self.sigma = std #std of the normal distribution, for uncertainty

    def update(self):
        self.object.x += self.object_speed_x
        self.object.y += self.object_speed_y
        self.object_speed_x = 0
        self.object_speed_y = 0
        if self.addText:
            self.text = self.addText2Block(self.text_string)

    def getpos(self): # return the normal distribution of the possible position
        pos = {}
        pos['x'] = np.random.normal(self.object.x, self.sigma, 1000)
        pos['y'] = np.random.normal(self.object.y, self.sigma, 1000)
        return pos
    
    def addText2Block(self, text):
        if self.text_string == None: 
            self.text_string = text
        self.text = FONT.render(self.text_string, pygame.Color(255, 203, 5)), (self.object.x, self.object.y+self.object_height/2)
        return self.text