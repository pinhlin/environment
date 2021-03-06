import pygame, sys, time, math
import numpy as np
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class Gripper(object):
    def __init__(self):
        self.gripper_mode = 'pick'
        self.gripper_size = 6
        self.gripper_height = 50
        self.gripper_init_width = 35
        self.gripper_width = 50
        self.gripping = False # bool to check if the gripper is gripping, if True, the 
                              # gripper stop to calculate its center (for pick up)
        #initial position of the gripper, at the center of the screen
        self.init_pos = [SCREEN_WIDTH/2, 100]#SCREEN_HEIGHT/2-50]
        self.gripperCenter = [SCREEN_WIDTH/2, 100]#SCREEN_HEIGHT/2-50]
        #gripper
        self.lg = pygame.Rect(self.gripperCenter[0]-self.gripper_width/2-self.gripper_size, self.gripperCenter[1], self.gripper_size, self.gripper_height)
        self.rg = pygame.Rect(self.gripperCenter[0]+self.gripper_width/2, self.gripperCenter[1], self.gripper_size, self.gripper_height)
        self.lg_speed_x = 0
        self.lg_speed_y = 0
        self.rg_speed_x = 0
        self.rg_speed_y = 0
        #stir constant
        self.stir_count = 100
        self.stir_speed = 1
        #pour constant
        self.pour_count = 200
        self.pour_speed = 10

    def getGripper(self): #get the information about gripper
        return (self.lg, self.rg)

    def gripper_center(self):
        self.gripperCenter[0] = self.rg.x - self.gripper_width / 2
        self.gripperCenter[1] = self.lg.y + self.gripper_height / 2

    def gripper_movement(self, dim):
        if dim == 'x':
            if self.lg.colliderect(self.rg) == False:
                self.gripper_width += self.rg_speed_x -self.lg_speed_x
                self.lg.x += self.lg_speed_x
                self.rg.x += self.rg_speed_x

        if dim == 'y':
                self.lg.y += self.lg_speed_y    
                self.rg.y += self.rg_speed_y
                
    def gripper_x_movement(self, target, target_width):
        if target == None:
            target_posx = target_width
        else:
            target_posx = target.x + target_width / 2
        if math.fabs(target_posx - self.gripperCenter[0]) > 0.5:
            if target_posx > self.gripperCenter[0]:
                self.lg_speed_x = 1
                self.rg_speed_x = 1
            elif target_posx < self.gripperCenter[0]:
                self.lg_speed_x = -1
                self.rg_speed_x = -1
        else:
            self.lg_speed_x = 0
            self.rg_speed_x = 0
        self.gripper_movement('x')

    def gripper_y_movement(self, target, target_height):
        target_posy = target.y# - target_height / 2
        if target_posy > self.gripperCenter[1]:
            self.lg_speed_y = 1
            self.rg_speed_y = 1
        elif target_posy < self.gripperCenter[1]:
            self.lg_speed_y = -1
            self.rg_speed_y = -1
        else:
            self.lg_speed_y = 0
            self.rg_speed_y = 0
        self.gripper_movement('y')

    def pick_up(self, target_class):
        target_width, target_height = (target_class.object_width, target_class.object_height)
        if target_width >= self.gripper_width and self.gripping == False:
            self.loose_gripper(target_width)
        else:
            target = target_class.hold
            if self.gripping == False:
                self.gripper_x_movement(target, target_width)
            if self.lg_speed_x == 0 and self.rg_speed_x == 0 or self.gripping:
                self.gripper_y_movement(target, target_height)
                if self.lg_speed_y == 0 and self.rg_speed_y == 0 or self.gripping:
                    self.gripping = True
                    if self.grip(target):
                        self.gripping = False
                        return True
        self.gripper_center()
        return False

    def back(self, target_class = None):
        target = None
        if target_class != None:
            target = target_class.object
        if self.lg.y > self.init_pos[1]:
            self.lg_speed_y = -1
            self.rg_speed_y = -1
            if target != None:
                target_class.object_speed_y = self.lg_speed_y
                target_class.update()
            self.gripper_movement('y')
        else:
            self.lg_speed_x = 0
            self.rg_speed_x = 0
            self.lg_speed_y = 0
            self.rg_speed_y = 0
            if target_class != None:
                target_class.object_speed_y = 0
            return True
        self.gripper_center()
        return False

    def grip(self, target):
        self.lg_speed_x = 1
        self.rg_speed_x = -1
        if self.lg.colliderect(target):
            self.lg_speed_x = 0
        if self.rg.colliderect(target):
            self.rg_speed_x = 0    
        self.gripper_movement('x')
        self.lg_speed_x = 0
        self.rg_speed_x = 0
        if self.lg.colliderect(target) and self.rg.colliderect(target):
            return True
        return False

    def loose_gripper(self, desired_width = None):
        if desired_width == None:
            desired_width = self.gripper_init_width

        if self.gripper_width <= desired_width:
            self.lg_speed_x -= 1
            self.rg_speed_x += 1
            self.gripper_movement('x')
            self.lg_speed_x = 0
            self.rg_speed_x = 0
            return False
        else:
            self.lg_speed_x = 0
            self.rg_speed_x = 0
            return True
        

    def put(self, target_class, beput_class, table = None):
        target = target_class.object
        if type(beput_class) is int:
            beput = table
            self.gripper_x_movement(None, beput_class)
        else:
            beput_width = beput_class.object_width
            beput = beput_class.bottom
            self.gripper_x_movement(beput, beput_width)
        if self.lg_speed_x == 0 and self.lg_speed_x == 0 or self.gripping:
            if target.colliderect(beput) == True:
                self.gripping = True
                self.lg_speed_y = 0
                self.rg_speed_y = 0
                if self.loose_gripper():
                    self.gripping = False
                    target_class.object_speed_x = 0
                    target_class.object_speed_y = 0
                    return True
                return False
            else:
                self.lg_speed_y = 1
                self.rg_speed_y = 1
                self.gripper_movement('y')
        target_class.object_speed_x = self.lg_speed_x
        target_class.object_speed_y = self.lg_speed_y
        target_class.update()
        self.gripper_center()
        return False

    def stir(self, target_class):
        if self.stir_count % 10 == 0:
            self.stir_speed = -1*self.stir_speed
        self.lg_speed_x = self.stir_speed
        self.rg_speed_x = self.stir_speed
        self.gripper_movement('x')
        self.lg_speed_x = 0
        self.rg_speed_x = 0 
        self.gripper_center()
        target_class.object_speed_x = self.stir_speed
        target_class.update()
        self.stir_count -= 1
        if self.stir_count == 0:
            self.stir_count = 100
            self.lg_speed_x = 0
            self.rg_speed_x = 0 
            return True
        return False

    def shake(self, target_class):
        if self.pour_count % 10 == 0:
            self.pour_speed = -1*self.pour_speed
        self.lg_speed_y = self.pour_speed
        self.rg_speed_y = self.pour_speed
        self.gripper_movement('y')
        self.lg_speed_y = 0
        self.rg_speed_y = 0 
        self.gripper_center()
        target_class.object_speed_y = self.pour_speed
        target_class.update()
        self.pour_count -= 1
        if self.pour_count == 0:
            self.pour_count = 100
            self.lg_speed_y = 0
            self.rg_speed_y = 0 
            return True
        return False

    def pour(self, target_class, beput_class, table = None):
        if type(beput_class) is int:
            beput = table
            self.gripper_x_movement(None, beput_class)
        else:
            beput_width = beput_class.object_width
            beput = beput_class.bottom
            self.gripper_x_movement(beput, beput_width)
        if self.lg_speed_x == 0 and self.lg_speed_x == 0:
            return self.shake(target_class)
        target_class.object_speed_x = self.lg_speed_x
        target_class.object_speed_y = self.lg_speed_y
        target_class.update()
        self.gripper_center()
        return False

    def open_drawer(self, target_class, table):
        if target_class.object.colliderect(table):
            self.lg_speed_y = -1
            self.rg_speed_y = -1
            target_class.object_speed_y = self.lg_speed_y
            self.gripper_movement('y')
            target_class.update()
        else:
            self.lg_speed_x = 0
            self.rg_speed_x = 0
            self.lg_speed_y = 0
            self.rg_speed_y = 0
            if target_class != None:
                target_class.object_speed_y = 0
            return True
        self.gripper_center()
        return False
        
    def close_drawer(self, drawer, val):
        if drawer.object.y < val:
            self.lg_speed_y = 1
            self.rg_speed_y = 1
            drawer.object_speed_y = self.lg_speed_y
            self.gripper_movement('y')
            drawer.update()
        else:
            self.lg_speed_x = 0
            self.rg_speed_x = 0
            self.lg_speed_y = 0
            self.rg_speed_y = 0
            if drawer != None:
                drawer.object_speed_y = 0
            return True
        self.gripper_center()
        return False