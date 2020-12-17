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
        # PyGame Initialization
        pygame.display.init()
        self.clock = pygame.time.Clock()
        self.gui = Gui()
        self.gripper = Gripper()
        self.plan = []
        self.cur_plan = []
        self.cur_action = ''
        self.target_name = None
        self.beput_name = None
        self.action_status = True #to check if the current action is done  
        self.plan_status = True #to check if the plan is done  
        #self.in_grip_obj = None #None if there is no object in the gripper 
        #      
    def pour(self, bepour, target):
        self.cur_plan.append('pouring')
        self.plan += ['pour', target, bepour]
        self.plan_status = False
        self.run()

    def fill_water(self, target, faucet):
        self.cur_plan.append('filling water')
        self.plan += ['pick', target, 'back', target, 'put', target, faucet, 'fill_water', 'none']
        self.plan_status = False
        self.run()

    def stir(self, target, bestir):
        self.cur_plan.append('stirring')
        self.plan += ['put', target, bestir, 'pick', target, 'stir', target, 'back', target]
        self.plan_status = False
        self.run()

    def pick_up(self, target):
        """
        Adds `pick up` operation to existing plan;
        Picks up `target`.
        Input: `target`, a string denoting target object
        """
        self.cur_plan.append('picking up target')
        self.plan += ['pick', target, 'back', target]
        self.plan_status = False
        self.run()

    def put(self, target, beput):
        """
        Adds `put` operation to existing plan;
        Puts `beput` onto `target`.
        Input:  `target`, a string denoting target platform
                `beput`, string denoting object to be put 
        """
        self.cur_plan.append('putting target')
        self.plan += ['put', target, beput, 'back', 'none']
        self.plan_status = False
        self.run()

    def open_drawer(self, target):
        self.cur_plan.append('opening drawer')
        self.plan += ['pick', target, 'open', target]
        self.plan_status = False
        self.run()

    def close_drawer(self, target):
        self.cur_plan.append('closing drawer')
        self.plan += ['pick', target, 'close', target]
        self.plan_status = False
        self.run()

    def _execute_plan(self):
        """
        If the last action was completed, pop the next action from our plan.
        Execute the action.
        """
        if self.action_status and len(self.plan):
            self.cur_action = self.plan.pop(0)
            self.target_name = self.plan.pop(0)
            if self.cur_action == 'put' or self.cur_action == 'pour':
                self.beput_name = self.plan.pop(0)
        self.action_status = self.gui.executeAction(self.gripper, self.cur_action, self.target_name, self.beput_name)
        #if the last action of the plan is done
        if self.action_status and len(self.plan) == 0:
            self.plan_status = True

    def run(self):
        """
        Run the kitchen environment and display it.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.plan_status == False:
                self._execute_plan()
            self.gui.draw(self.gripper, self.cur_action)
            pygame.display.flip()
            self.clock.tick(60)
            if self.plan_status:
                break
        