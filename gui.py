import pygame, sys, time
import stuff
from gripper import Gripper
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class Gui(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.font.init()
        #to check if current action is pouring
        #self.rotate = False
        #self.rotate_count = 200
        # setting background color
        self.bg_color = pygame.Color('grey12')
        self.light_grey = (200, 200, 200)
        self.dark_grey = (120, 120, 120)
        self.groundline = (255, 255, 255)
        # loading background
        # self.background = pygame.image.load('maize_blue.jpg')
        self.gui_list = [] #to collect all the object in the gui
        self.name2obj = {} #a dict to help to convert object name to object
        #table
        self.table = pygame.Rect(0, SCREEN_HEIGHT-50, SCREEN_WIDTH, 50)
        self.gui_list.append((self.bg_color, self.table))
        #spoon
        height = 100
        self.spoon = stuff.spoon('white', 5, height, 50, SCREEN_HEIGHT-50-height-10)
        self.gui_list.append((self.spoon.color, self.spoon.shaft))
        self.gui_list.append((self.spoon.color, self.spoon.head))
        self.name2obj['spoon'] = self.spoon
        #cup
        self.cup = stuff.cup('white', 40, 60, 200)
        self.contain_color = self.bg_color
        self.gui_list.append(('dummy_color', self.cup.object))
        self.gui_list.append((self.cup.color, self.cup.left))
        self.gui_list.append((self.cup.color, self.cup.right))
        self.gui_list.append((self.cup.color, self.cup.bottom))
        self.name2obj['cup'] = self.cup
        #block1
        self.block = stuff.block('brown', 50, 80, 100, SCREEN_HEIGHT-50-80)
        self.gui_list.append(('brown', self.block.object))
        self.name2obj['coffee'] = self.block

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
        if action == 'fill_water':
            self.contain_color = (0, 0, 255)
            done = True
        if action == 'stir':
            r, g, b = self.contain_color
            r = min(165, r+3)
            g = min(42, g+1)
            b = max(42, b-5)
            self.contain_color = (r, g, b)
            done = gripper.stir(target)
        if action == 'pick':
            done = gripper.pick_up(target)
        if action == 'back':
            done = gripper.back(target)
        if action == 'put':
            if type(beput_name) is str:
                done = gripper.put(target, self.name2obj[beput_name])
            else:
                done = gripper.put(target, beput_name, self.table)
        if action == 'pour':
            done =  gripper.move_x(target, self.name2obj[beput_name])

        return done

    def getGui(self): #get the information of the gui
        return self.gui_list

    def draw(self, gripper, action):
        left_gripper, right_gripper = gripper.getGripper()
        # visuals
        self.screen.fill(self.bg_color)
        # setting background
        # self.screen.blit(self.background, (0, 0))
        lg = pygame.Surface((left_gripper.w, left_gripper.h))
        rg = pygame.Surface((right_gripper.w, right_gripper.h))
        lg.fill(self.light_grey)
        rg.fill(self.light_grey)
        self.screen.blit(lg, [left_gripper.x, left_gripper.y])
        self.screen.blit(rg, [right_gripper.x, right_gripper.y])
        pygame.draw.aaline(self.screen, self.groundline, (0, SCREEN_HEIGHT-50),(SCREEN_WIDTH, SCREEN_HEIGHT-50))
        #print curretn action
        font = pygame.font.SysFont('freesansbold.ttf', 32) 
        text = font.render('current action is: ' + action, True, (0, 255, 0), (0, 0, 255)) 
        textRect = text.get_rect()  
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) 
        self.screen.blit(text, textRect)
        for information in self.gui_list:
            color, obj = information
            if color == 'dummy_color':
                color = self.contain_color
            surf = pygame.Surface((obj.w, obj.h))
            surf.fill(color)
            self.screen.blit(surf, [obj.x, obj.y])
        
        """
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

                if self.rotate:
            angle = 0
            while self.rotate_count >= 0:
                self.rotate_count -= 1
                if self.rotate_count % 20 == 0:
                    angle -= 1
                rotated_lg = pygame.transform.rotate(lg, angle)
                rotated_rg = pygame.transform.rotate(rg, angle)
                self.screen.blit(rotated_lg, [left_gripper.x, left_gripper.y])
                self.screen.blit(rotated_rg, [right_gripper.x, right_gripper.y])
            self.rotate_count = 200
            self.rotate = False
        else:
        """