import pygame, sys, time
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
class gripper(object):
    def __init__(self):
        self.gripper_mode = 'pick'
        self.gripper_size = 1
        self.gripper_height = 50
        self.gripper_init_width = 35
        self.gripper_width = 35
        #initial position of the gripper, at the center of the screen
        self.init_pos = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        self.gripperCenter = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
        #gripper
        self.lg = pygame.Rect(self.gripperCenter[0]-self.gripper_width/2, self.gripperCenter[1], self.gripper_size, self.gripper_height)
        self.rg = pygame.Rect(self.gripperCenter[0]+self.gripper_width/2, self.gripperCenter[1], self.gripper_size, self.gripper_height)
        self.lg_speed_x = 0
        self.lg_speed_y = 0
        self.rg_speed_x = 0
        self.rg_speed_y = 0

    def getGripper(self): #get the information about gripper
        return (self.lg, self.rg)

    def gripper_center(self):
        self.gripper_width += self.rg_speed_x -self.lg_speed_x
        self.gripperCenter[0] += (self.lg_speed_x + self.rg_speed_x) / 2
        self.gripperCenter[1] += (self.lg_speed_y + self.rg_speed_y) / 2

    def gripper_movement(self, dim):
        if dim == 'x':
            if self.lg.x != self.rg.x:
                self.lg.x += self.lg_speed_x
                self.rg.x += self.rg_speed_x

        if dim == 'y':
                self.lg.y += self.lg_speed_y    
                self.rg.y += self.rg_speed_y
                
    def gripper_x_movement(self, target, target_width):
        target_posx = target.x + target_width / 2
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
        target_posy = target.y - target_height / 2
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
        target = target_class.object
        self.gripper_x_movement(target, target_width)
        if self.lg_speed_x == 0 and self.rg_speed_x == 0:
            self.gripper_y_movement(target, target_height)
            if self.lg_speed_y == 0 and self.rg_speed_y == 0:
                if self.lg.colliderect(target) and self.rg.colliderect(target):
                    self.lg_speed_x = 0
                    self.rg_speed_x = 0
                    return True
                else:
                    if self.lg.colliderect(target) == False:
                        self.lg_speed_x += 1
                    else:
                        self.lg_speed_x = 0
                    if self.rg.colliderect(target) == False:
                        self.rg_speed_x -= 1
                    else:
                        self.rg_speed_x = 0
                    self.gripper_movement('x')
        self.gripper_center()
        return False       

    def back(self, target_class = None):
        target = target_class.object
        if self.lg.y > self.init_pos[1]:
            self.lg_speed_y = -1
            self.rg_speed_y = -1
            if target != None:
                target.y += self.lg_speed_y
            self.gripper_movement('y')
        else:
            self.lg_speed_x = 0
            self.rg_speed_x = 0
            self.lg_speed_y = 0
            self.rg_speed_y = 0
            return True
        return False

    def loose_gripper(self):
        while self.gripper_width < self.gripper_init_width:
            self.lg_speed_x -= 1
            self.rg_speed_x += 1
            self.gripper_movement('x')
            self.gripper_center()

    def put(self, target_class, beput):
        target = target_class.object
        beput_width = beput.platform_width
        self.gripper_x_movement(beput, beput_width)
        if self.lg_speed_x == 0 and self.lg_speed_x == 0:
            if target.colliderect(beput) == True:
                self.lg_speed_y = 0
                self.rg_speed_y = 0
                self.loose_gripper()
                self.lg_speed_x = 0
                self.rg_speed_x = 0
                return True
            else:
                self.lg_speed_y = 1
                self.rg_speed_y = 1
                self.gripper_movement('y')
        target.x += self.lg_speed_x
        target.y += self.lg_speed_y
        return False

"""
    def objMovement(self):
        #updating the gripper center
        self.gripper_center()
        if self.gripper_mode == 'pick':
            if self.pick_up(self.object, (self.object_width, self.object_height)):
                self.gripper_mode = 'back'
        
        if self.gripper_mode == 'back':
            if self.back(self.object):
                self.gripper_mode = 'put'
        
        if self.gripper_mode == 'put':
            if(self.put(self.object, self.target_platform, (self.platform_width, self.platform_height))):
                if(self.back()):
                    self.gripper_mode = 'pick'
                    #can be deleted for the future use
                    if self.target_platform == self.platform_org:
                        self.target_platform = self.platform
                    else:
                        self.target_platform = self.platform_org
                        
"""

                


