import pygame, sys, time
import stuff
import test
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class gui(object):
    def __init__(self): 
        self.gui_list = [] #to collect all the object in the gui
        self.name2obj = {} #a dict to help to convert object name to object
        #block
        self.block = stuff.block('white', 26, 50, 100, 330)
        self.gui_list.append((self.block.color, self.block.object))
        self.name2obj['object1'] = self.block
        #platform_orginal
        self.platform_org = stuff.platform('red', 50, 50, 88, 380)
        self.gui_list.append((self.platform_org.color, self.platform_org.platform))
        self.name2obj['plt_org'] = self.platform_org
        #platform_target
        self.platform_target = stuff.platform('blue', 50, 50, SCREEN_WIDTH / 2 - 25, 380)
        self.gui_list.append((self.platform_target.color, self.platform_target.platform))
        self.name2obj['plt_taret'] = self.platform_target

    def executeAction(self, gripper, action = None, target_name = None):
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
            done == gripper.back(target)
        #if action == 'put':
        #   done == gripper.put(target)
        return done

    def getGui(self): #get the information of the gui
        return self.gui_list

        
