import gui
import test
import pygame, sys, time
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class env(object):
    def __init__(self):
        self.gripper = test.gripper()
        self.gui = gui.gui()
        #simple plan, can be modified for future purpose
        self.plan = ['pick','object1','back','object1','put','object1','plt_target', 'back', 'none',\
                        'pick','object2','back','object2','put', 'object2','object1','back', 'none'] 
        self.cur_action = None
        self.target_name = None
        self.beput_name = None
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        #setting background color
        self.bg_color = pygame.Color('grey12')
        self.light_grey = (200, 200, 200)
        self.dark_grey = (120, 120, 120)
        self.groundline = (255, 255, 255)
        self.action_status = True #to check if the current action is done
        #loading background
        #self.background = pygame.image.load('maize_blue.jpg')

    def executePlan(self):
        #if the last action is completed, pop out the next action
        #if there is a target, the target must follows right behind
        #the action
        if self.action_status and len(self.plan):
            self.cur_action = self.plan.pop(0)
            self.target_name = self.plan.pop(0)
            if self.cur_action == 'put': #if the action is "put", need to have the platform
                self.beput_name = self.plan.pop(0)
        self.action_status = self.gui.executeAction(self.gripper, self.cur_action, self.target_name, self.beput_name)
        #print(self.action_status)
        return self.action_status

    def animation(self):
        self.executePlan()
        #get the information in the environment
        left_gripper, right_gripper = self.gripper.getGripper()
        gui_list = self.gui.getGui()
        #visuals
        self.screen.fill(self.bg_color)
        #setting background
        #self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, self.light_grey, left_gripper)
        pygame.draw.rect(self.screen, self.light_grey, right_gripper)
        for information in gui_list:
            color, obj = information
            pygame.draw.rect(self.screen, color, obj)
            
        pygame.draw.aaline(self.screen, self.groundline, (0, SCREEN_HEIGHT-50),(SCREEN_WIDTH, SCREEN_HEIGHT-50))
        #pygame.draw.aaline(self.screen, self.light_grey, (self.screen_width / 2, 0),(self.screen_width / 2, self.screen_height))