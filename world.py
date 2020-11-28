import pygame, sys, time
from gripper import Gripper
from gui import Gui

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class Kitchen(object):
    """
    Kitchen environment for Kitchen for Progress 2D.
    Serves as main API interface.
    """
    def __init__(self):
        self.gripper = Gripper()
        self.gui = Gui()
        self.plan = [] 
        self.cur_action = None
        self.target_name = None
        self.beput_name = None
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # setting background color
        self.bg_color = pygame.Color('grey12')
        self.light_grey = (200, 200, 200)
        self.dark_grey = (120, 120, 120)
        self.groundline = (255, 255, 255)
        self.action_status = True #to check if the current action is done
        # loading background
        # self.background = pygame.image.load('maize_blue.jpg')

    def pick_up(self, target):
        """
        Adds `pick up` operation to existing plan;
        Picks up `target`.
        Input: `target`, a string denoting target object
        """
        self.plan = self.plan + ['pick', target, 'back', target]

    def put(self, target, beput):
        """
        Adds `put` operation to existing plan;
        Puts `beput` onto `target`.
        Input:  `target`, a string denoting target platform
                `beput`, string denoting object to be put 
        """
        self.plan = self.plan + ['put', target, beput, 'back', 'none']

    def executePlan(self):
        """
        If the last action was completed, pop the next action from our plan.
        Execute the action.
        """
        if self.action_status and len(self.plan):
            self.cur_action = self.plan.pop(0)
            self.target_name = self.plan.pop(0)
            if self.cur_action == 'put':
                self.beput_name = self.plan.pop(0)
        self.action_status = self.gui.executeAction(self.gripper, self.cur_action, self.target_name, self.beput_name)

    def animation(self):
        """
        Run the existing plan and display it.
        """
        self.executePlan()
        # get the information in the environment
        left_gripper, right_gripper = self.gripper.getGripper()
        gui_list = self.gui.getGui()
        # visuals
        self.screen.fill(self.bg_color)
        # setting background
        # self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, self.light_grey, left_gripper)
        pygame.draw.rect(self.screen, self.light_grey, right_gripper)
        for information in gui_list:
            color, obj = information
            pygame.draw.rect(self.screen, color, obj)
            
        pygame.draw.aaline(self.screen, self.groundline, (0, SCREEN_HEIGHT-50),(SCREEN_WIDTH, SCREEN_HEIGHT-50))