import pygame, sys, time
import pygame.freetype
from objects import Spoon, Cup, Drawer, Block
from gripper import Gripper
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class Gui(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.freetype.init()
        #to check if current action is pouring
        #self.rotate = False
        #self.rotate_count = 200
        # setting background color
        self.bg_color = pygame.Color('white') #pygame.Color('grey12')
        self.light_grey = (200, 200, 200)
        self.dark_grey = (120, 120, 120)
        self.groundline = (0,0,0)
        self.maize = pygame.Color(255, 203, 5)
        self.blue = pygame.Color(0, 39, 76)
        self.table_color = self.blue#pygame.Color(202, 164, 114)
        # loading background
        # self.background = pygame.image.load('maize_blue.jpg')
        self.gui_list = [] #to collect all the object in the gui
        self.name2obj = {} #a dict to help to convert object name to object
        self.drawers_list = [] # a list to collect all the drawer names for closing
        # define drawers constants and locations:
        self.drawer_height = 120
        self.drawer_width = 80
        self.drawer_front = SCREEN_HEIGHT-50-10
        self.drawer_bottom = self.drawer_front + self.drawer_height
        self.drawer_pos_coffee = 115
        self.drawer_pos_cup = 215
        self.drawer_pos_spoon = 15

        # spoon
        height = 100
        self.spoon = Spoon(self.blue, 5, height, self.drawer_pos_spoon+self.drawer_width/2, 
                                self.drawer_bottom-height-10)

        # cup
        cup_height = 60
        cup_width = 40
        self.cup = Cup(self.blue, cup_width, cup_height, self.drawer_pos_cup+self.drawer_width/2-cup_width/2, self.drawer_bottom)
        self.contain_color = self.bg_color
        self.coffee_color = self.bg_color

        # coffee
        bag_height = 80
        bag_width = 50
        self.coffee_bag = Block(self.blue, bag_width, bag_height, self.drawer_pos_coffee+self.drawer_width/2-bag_width/2, \
                                    self.drawer_bottom-bag_height, addText=True)
        self.coffee_bag.addText2Block('Coffee')
        # drawer1
        self.drawer1 = Drawer(self.maize, self.drawer_width, self.drawer_height, self.drawer_pos_coffee, self.drawer_front, self.coffee_bag)
        self.gui_list.append((self.maize, self.drawer1.object, self.drawer1))
        self.gui_list.append(('black', self.drawer1.bottom, self.drawer1))
        self.name2obj['drawer1'] = self.drawer1
        self.drawers_list.append('drawer1')
        # drawer2
        self.drawer2 = Drawer(self.maize, self.drawer_width, self.drawer_height, self.drawer_pos_cup, self.drawer_front, self.cup)
        self.gui_list.append((self.maize, self.drawer2.object, self.drawer2))
        self.name2obj['drawer2'] = self.drawer2
        self.drawers_list.append('drawer2')
        # drawer3
        self.drawer3 = Drawer(self.maize, self.drawer_width, self.drawer_height, self.drawer_pos_spoon, self.drawer_front, self.spoon)
        self.gui_list.append((self.maize, self.drawer3.object, self.drawer3))
        self.name2obj['drawer3'] = self.drawer3
        self.drawers_list.append('drawer3')

        #appending object in the list after drawer
        #appending coffee
        self.gui_list.append((self.blue, self.coffee_bag.object, self.coffee_bag))
        self.name2obj['coffee'] = self.coffee_bag 
        #appending cup
        self.gui_list.append(('dummy_color', self.cup.object, self.cup))
        self.gui_list.append(('dummy_coffee', self.cup.coffee, self.cup))
        self.gui_list.append((self.cup.color, self.cup.left, self.cup))
        self.gui_list.append((self.cup.color, self.cup.right, self.cup))
        self.gui_list.append((self.cup.color, self.cup.bottom, self.cup))
        self.name2obj['cup'] = self.cup
        #spoon
        self.gui_list.append((self.spoon.color, self.spoon.shaft, self.spoon))
        self.gui_list.append((self.spoon.color, self.spoon.head, self.spoon))
        self.name2obj['spoon'] = self.spoon
        # table
        self.table = pygame.Rect(0, SCREEN_HEIGHT-50, SCREEN_WIDTH, 50)
        self.gui_list.append((self.table_color, self.table, None))

        #faucet
        faucet_ul_x, faucet_ur_x = SCREEN_WIDTH-150, SCREEN_WIDTH-50
        faucet_bl_x, faucet_br_x = SCREEN_WIDTH-150, SCREEN_WIDTH-50
        faucet_ul_y, faucet_ur_y =  SCREEN_HEIGHT-50-200, SCREEN_HEIGHT-50-200
        faucet_bl_y, faucet_br_y = SCREEN_HEIGHT-50, SCREEN_HEIGHT-50
        self.faucet_coordinates = [(faucet_ul_x,faucet_ul_y), (faucet_ur_x, faucet_ur_y),
                                (faucet_br_x, faucet_br_y), (faucet_br_x-30,faucet_br_y),
                                (faucet_br_x-30, faucet_ur_y+30), (faucet_ul_x+30,faucet_ul_y+30),
                                (faucet_ul_x+30,faucet_ul_y+40), (faucet_ul_x,faucet_ul_y+40)]
        self.color_table = {
            'dummy_color' : self.contain_color,
            'dummy_coffee' : self.coffee_color
        }


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
            self.contain_color = pygame.Color(186, 229, 225, 10)
            self.color_table['dummy_color'] = self.contain_color
            done = True
        if action == 'stir':
            r, g, b, a = self.contain_color
            r = min(165, r+3)
            g = min(42, g+1)
            b = max(42, b-2)
            self.contain_color = pygame.Color(r, g, b, a)
            self.color_table['dummy_color'] = self.contain_color
            self.color_table['dummy_coffee'] = self.contain_color
            done = gripper.stir(target)
        if action == 'pick':
            done = gripper.pick_up(target)
        if action == 'back':
            done = gripper.back(target)
        if action == 'put':
            if type(beput_name) is str:
                if beput_name == 'faucet':
                    done = gripper.put(target, SCREEN_WIDTH-130, self.table)
                else:
                    done = gripper.put(target, self.name2obj[beput_name])
                    if beput_name in self.drawers_list:
                        drawer = self.name2obj[beput_name]
                        drawer.contain = target
            else:
                done = gripper.put(target, beput_name, self.table)
        if action == 'pour':
            done =  gripper.pour(target, self.name2obj[beput_name])
            if done:
                self.coffee_color = pygame.Color(202, 164, 114)
                self.color_table['dummy_coffee'] = self.coffee_color
        if action == 'open':
            done = gripper.open_drawer(target, self.table)
            if done:
                target.contain = None
        if action == 'close':
            print(1)
            done = gripper.close_drawer(target, self.name2obj[beput_name], self.drawer_front)

        return done

    def getGui(self): #get the information of the gui
        return self.gui_list

    def draw(self, gripper, action):
        left_gripper, right_gripper = gripper.getGripper()
        # visuals
        self.screen.fill(self.bg_color)
        # setting background
        # self.screen.blit(self.background, (0, 0))
        #draw the faucet
        pygame.draw.polygon(self.screen, 'grey', self.faucet_coordinates)
        # TODO: Fix this - I don't think this works?
        pygame.draw.aaline(self.screen, self.groundline, (0, SCREEN_HEIGHT-50),(SCREEN_WIDTH, SCREEN_HEIGHT-50))

        font = pygame.freetype.Font('fonts/OpenSans-Light.ttf', 24) 
        text, text_rect = font.render('current action: ' + action, fgcolor=self.blue)
        text_rect.center = (SCREEN_WIDTH // 2, 20)
        self.screen.blit(text, text_rect)

        for information in self.gui_list:
            color, obj, obj_class = information
            if type(color) == str and color in self.color_table.keys():
                color = self.color_table[color]
            surf = pygame.Surface((obj.w, obj.h))
            surf.fill(color)
            self.screen.blit(surf, [obj.x, obj.y])
            if obj_class != None:
                if obj_class.addText:
                    text, text_rect = obj_class.text
                    self.screen.blit(text[0], text_rect)
        lg = pygame.Surface((left_gripper.w, left_gripper.h))
        rg = pygame.Surface((right_gripper.w, right_gripper.h))
        lg.fill(self.light_grey)
        rg.fill(self.light_grey)
        self.screen.blit(lg, [left_gripper.x, left_gripper.y])
        self.screen.blit(rg, [right_gripper.x, right_gripper.y])