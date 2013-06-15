"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
from world import MAP_TILE_WIDTH, MAP_TILE_HEIGHT
from random import randint
import math
import copy

# Own imports
import utils

class GameObject(pygame.sprite.Sprite):
    """Abstract superclass for all objects in the game."""
    world = None
    def __init__(self, position, frames, real_rect = None):
        super(GameObject, self).__init__()
        self.image = frames[0][0]
        self.rect = self.image.get_rect()
        if real_rect == None:
            self.real_rect = self.image.get_rect()
        else:
            self.real_rect = real_rect

        self._offset = real_rect.topleft
        self.pos = utils.Point(position[0], position[1])
        if frames:
            self.frames = frames

        self.animation = self.stand_animation()
        self.speed = 2
        self.animation_counter = 0
        self.animation_speed = 8 #higher is slower, like wut

    @property
    def tile_pos(self):
        """Return the tile that corresponds to this object's position."""
        return utils.Point(int(self.pos.x / MAP_TILE_WIDTH),
                           int(self.pos.y / MAP_TILE_HEIGHT))

    def _get_pos(self):
        """Check the current position of the sprite on the map."""
        return self._pos

    def _set_pos(self, position):
        """Set the position and depth of the sprite on the map."""
        self._pos = utils.Point(position[0], position[1])
        self.rect.x = self._pos[0]
        self.rect.y = self._pos[1]
        self.real_rect.x = self._pos[0] + self._offset[0]
        self.real_rect.y = self._pos[1] + self._offset[1]
        self.depth = self.real_rect.midbottom[1]

    # Use special getters and setters for pos, that adjust the rect as well
    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""
        self.pos += (dx, dy)

    def collision_move(self, level, dx, dy):
        """Change the position of the sprite on screen."""
        self.pos += (dx, dy)
        if not level.valid_position(self):
            self.pos += (-dx, 0)
            if not level.valid_position(self):
                self.pos += (dx, -dy)
                if not level.valid_position(self):
                    self.pos += (-dx, 0)

    def stand_animation(self, direction = 0):
        """The default animation."""

        while True:
            # Change to next frame every two ticks
            for frame in self.frames[0]:
                self.image = frame
                yield None
                yield None

    def animation_speed_check(self):
        if self.animation_counter < self.animation_speed:
            self.animation_counter += 1
            return False
        else:
            self.animation_counter = 0
            return True

    def update(self, *args): # TODO use/remove *args
        """Run the current animation."""

        if self.animation_speed_check():
            self.animation.next()

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__,
                               self.pos[0], self.pos[1])

    def __str__(self):
        return self.__repr__()

class Person(GameObject):
    """Class for one person."""

    def __init__(self, position, image, rect):
        GameObject.__init__(self, position, image, rect)
        self.final_goal = (40, 200)
        self.goal = None
        self.direction = 2
        self.animation = None
        self.image = self.frames[self.direction][0]
        self.path = None
        self.idle = True
        self.angle = 0
        self.cone_angle = 10
        self.turn_angle = 45
        self.cone_length = 50
        self.return_angle = 5
        self.max_angle = 180
        self.move_vector = (0, 0)
        
    def walk_to_place(self, level, goal):
        """walk to goal in straight line, depending on self.speed"""
        DX = self.pos[0] - goal[0]
        DY = self.pos[1] - goal[1]
        total_length = (DX**2 + DY**2)**0.5
        dx = -1 * self.speed / total_length * DX
        dy = -1 * self.speed / total_length * DY
        dx,  dy = utils.rot_vector((dx,dy), self.angle)#this creates steering
        self.move_vector = (dx,dy)
        self.change_direction(dx, dy)
        self.collision_move(level, dx, dy)

    def change_direction(self, dx, dy):
        """ change self.direction depending on .., well, direction!"""
        if abs(dx*2) > abs(dy):
            if dx < 0:
                self.direction = 3
            else:
                self.direction = 1
        else:
            if dy < 0:
                self.direction = 0
            else:
                self.direction = 2

    def walk_animation(self):
        """Animation for the person walking."""
        # This animation is hardcoded for 4 frames and 16x24 map tiles
        for frame in range(4):
            self.image = self.frames[self.direction][frame]
            yield None

    def boundcheck(self, x, y):
        """checks if x and y are within screen bounds ( hardcoded for now)"""
        x = x if x > 0 else 0
        x = x if x < 1120 else 1120 -10
        y = y if y > 0 else 0
        y = y if y < 320 else 320 -10
        return x, y

    def get_cone_lines(self):
        """returns start and endpoint of the lines of the cone"""
        dx = self.move_vector[0]*self.cone_length
        dy = self.move_vector[1]*self.cone_length
        obj_pos = utils.Point(self.real_rect.center[0],self.real_rect.center[1])
        line_end_center = obj_pos + (dx, dy)
        dx, dy = utils.rot_vector((dx,dy),-1*self.cone_angle)
        line_end_left = obj_pos + (dx, dy)        
        dx, dy = utils.rot_vector((dx,dy), 2*self.cone_angle)
        line_end_right = obj_pos + (dx, dy)
        return (obj_pos, line_end_center),(obj_pos, line_end_left),(obj_pos, line_end_right)
    
    def get_bumper_hits(self, center, left, right, level):
        start = center[0]
        object_list =  level.game_objects 
        rect_list =  level.wall_rects 
        hit_center = False
        hit_left = False
        hit_right = False
        
        if object_list:
            for obj in object_list:
                if obj is not self:
                    if isinstance(obj, Person):
                        if not hit_center:
                            if utils.line_intersects_rect(start, center[1],obj.real_rect):
                                hit_center = True
                        if not hit_left:
                            if utils.line_intersects_rect(start, left[1],obj.real_rect):
                                hit_left = True
                        if not hit_right: 
                            if utils.line_intersects_rect(start, right[1],obj.real_rect):
                                hit_right = True
        """                        
        if rect_list:#this will also check for walls
            for rect in rect_list:
                if not hit_center:
                    if utils.line_intersects_rect(start, center[1],rect):
                        hit_center = True
                if not hit_left:
                    if utils.line_intersects_rect(start, left[1],rect):
                        hit_left = True
                if not hit_right: 
                    if utils.line_intersects_rect(start, right[1],rect):
                        hit_right = True
        """            
        return hit_center, hit_left, hit_right
        
    def line_hits_wall_rects(self, p1, p2, level):
        rect_list = level.wall_rects
        if rect_list:   #this check for walls
            for rect in rect_list:
                if utils.line_intersects_rect(p1, p2, rect):
                    return True
                    
    def fix_angle(self, angle):
        new_angle = None
        if angle > 360:
            new_angle = angle % 360
        elif angle < -360:
            new_angle = angle % -360
        else:
            new_angle = angle
        return new_angle
        
    def angle_decrease(self):
        if 0< self.angle < self.return_angle or 0 > self.angle > -1*self.return_angle: #if  angle is close to 0, set angle to 0 (prevent overshoot)
            self.angle = 0
        elif self.angle > 0:
            self.angle -= self.return_angle
        elif self.angle < 0:
            self.angle += self.return_angle


    def adjust_angle(self, hit_center, hit_left, hit_right):
        angle = 0
        if hit_center:
            if hit_right and not hit_left:                 #if someone is right infront of him and also to the right, or just infront of him
                angle += self.turn_angle * 2                #turn hard left
            elif hit_left and not hit_right:               #if someone is right infront of him and also to the left
                angle += self.turn_angle *-2                #turn hard right
            elif hit_left and hit_right:                   #if all frontal directions blocked
                r = 2 if randint(0,1) == 1 else -2
                angle += self.turn_angle * r                 #turn really hard left or right
            else: #must be only infront of him
                r = 1 if randint(0,1) == 1 else -1        #turn slightly left or right
                angle += self.turn_angle * r   
        elif hit_left:                                      #if someone is front/left of him only
            angle += self.turn_angle *-1                    #turn slightly right
        elif hit_right:                                     #if someone is front/right of him only
            angle += self.turn_angle * 1                    #turn slightly left

        
        
        if not hit_center and not hit_left and not hit_right:#if nothing is hit
            self.angle_decrease()                                #return to no rotation
            self.speed = 2
        else:
            newangle = angle +self.angle
            if newangle > self.max_angle:
                newangle = self.max_angle
            if newangle < -1*self.max_angle:
                newangle = -1*self.max_angle
                
            self.angle = newangle #adjust self.angle
            self.speed = 1
            
    def update(self, level):
        
        center, left, right = self.get_cone_lines() #get line segments of cone
        hit_center, hit_left, hit_right = self.get_bumper_hits(center, left, right, level)#see which line of cone is hit
        self.adjust_angle(hit_center, hit_left, hit_right)#adjust angle
        self_pos = utils.Point(self.real_rect.topleft[0],self.real_rect.topleft[1])
        
        if not self.path:
            self.path = level.plan_path(self_pos, self.final_goal)
        else:
            
            if self.animation is None:
                self.animation = self.walk_animation()
            adjusted_pos = utils.Point( self.path[0][0], self.path[0][1]) - self._offset
            self.walk_to_place(level, adjusted_pos) 
            
            if self.line_hits_wall_rects(self_pos, self.path[0], level):
                self.path = level.plan_path(self_pos, self.final_goal)
            
            if self_pos.dist(self.path[0]) < self.speed:
                del self.path[0]
                
            if self_pos.dist(self.final_goal) < self.speed:
                if len(self.final_goal) > 1:
                    self.final_goal = (1000, 200)

        if self.animation is None:
            self.image = self.frames[self.direction][0]
        else:
            try:
                if self.animation_speed_check():
                    self.animation.next()
            except StopIteration:
                self.animation = None

class Player(Person):
    """Player object."""

    def __init__(self, position, image, rect):
        Person.__init__(self, position, image, rect)
        self.direction = 2
        self.animation = None

    def update(self, level):
        """Run the current animation or just stand there if no animation set."""
        if self.animation is None:
            self.image = self.frames[self.direction][0]
        else:
            try:
                self.animation.next()
            except StopIteration:
                self.animation = None

class Cop(Person):
    """Cop object."""

    def __init__(self, pos, image, rect):
        Person.__init__(self, pos, image, rect)

    def update(self, level):
        # Logic here!
        pass
