import pygame, sys, time
import stuff
from gripper import Gripper
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class Gui(object):
    def __init__(self):
        self.gui_list = [] #to collect all the object in the gui
        self.name2obj = {} #a dict to help to convert object name to object
        #block1
        self.block = stuff.block('blue', 26, 50, 100, 330)
        self.gui_list.append((self.block.color, self.block.object))
        self.name2obj['object1'] = self.block
        #block2
        self.block = stuff.block('yellow', 26, 50, 583, 330)
        self.gui_list.append((self.block.color, self.block.object))
        self.name2obj['object2'] = self.block
        #platform_orginal1
        self.platform_org = stuff.platform('black', 50, 50, 88, 380)
        self.gui_list.append((self.platform_org.color, self.platform_org.object))
        self.name2obj['plt_org1'] = self.platform_org
        #platform_orginal2
        self.platform_org2 = stuff.platform('black', 50, 50, 560, 380)
        self.gui_list.append((self.platform_org2.color, self.platform_org2.object))
        self.name2obj['plt_org2'] = self.platform_org
        #platform_target
        self.platform_target = stuff.platform('red', 50, 50, SCREEN_WIDTH / 2 - 25, 380)
        self.gui_list.append((self.platform_target.color, self.platform_target.object))
        self.name2obj['plt_target'] = self.platform_target

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # setting background color
        self.bg_color = pygame.Color('grey12')
        self.light_grey = (200, 200, 200)
        self.dark_grey = (120, 120, 120)
        self.groundline = (255, 255, 255)
        # loading background
        # self.background = pygame.image.load('maize_blue.jpg')

    def executeAction(self, gripper, action = None, target_name = None, beput_name = None):
        if action == None and target_name == None:
            return False
        #setting the condition not having a target
        if target_name == 'none':
            target = None
        else:
            #convert string target name to object
            target = self.name2obj[target_name] 
        
        #action type is a string
        done = False
        if action == 'pick':
            done = gripper.pick_up(target)
        if action == 'back':
            done = gripper.back(target)
        if action == 'put':
            done = gripper.put(target, self.name2obj[beput_name])
        return done

    def getGui(self): #get the information of the gui
        return self.gui_list

    def draw(self, gripper):
        left_gripper, right_gripper = gripper.getGripper()
        # visuals
        self.screen.fill(self.bg_color)
        # setting background
        # self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, self.light_grey, left_gripper)
        pygame.draw.rect(self.screen, self.light_grey, right_gripper)
        for information in self.gui_list:
            color, obj = information
            pygame.draw.rect(self.screen, color, obj)
            
        pygame.draw.aaline(self.screen, self.groundline, (0, SCREEN_HEIGHT-50),(SCREEN_WIDTH, SCREEN_HEIGHT-50))
        
