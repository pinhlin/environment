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

    def _execute_plan(self):
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

    def run(self):
        """
        Run the existing plan and display it.
        """
        self._execute_plan()
        self.gui.draw(self.gripper)
        