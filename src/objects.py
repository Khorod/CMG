"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
from world import MAP_TILE_WIDTH, MAP_TILE_HEIGHT
from random import randint
# Own imports
import utils
import time
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
        self.animation_speed = 8 #higher is slower
    @property
    def _tile_pos(self):
        """Return the tile that corresponds to this object's position."""
        return utils.Point(self.pos.x / MAP_TILE_WIDTH, 
                           self.pos.y / MAP_TILE_HEIGHT)
        
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

    pos = property(_get_pos, _set_pos) # magic

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""
        self.pos += (dx, dy)
        
    def collision_move(self, level,dx, dy):
        """Change the position of the sprite on screen."""
        self.pos += (dx, dy)
        if not level.valid_position(self):
            self.pos +=(-dx, 0)
            if not level.valid_position(self):
                self.pos += (dx, -dy)
                if not level.valid_position(self):
                    self.pos += (-dx, 0)
                    
                    
    def stand_animation(self, direction = 0):
        """The default animation."""

        while True:
            # Change to next frame every two ticks
            for frame in self.frames[direction]:
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

class Person(GameObject):
    """Class for one person."""
    def __init__(self, position, image, rect):
        GameObject.__init__(self, position, image, rect)
        self.goal = None
        self.direction = 2
        self.animation = None
        self.image = self.frames[self.direction][0]
        #path to follow
        self.path = [(500,150),(600,150)]#[(0,0), (1100,5), (1100, 300), (0, 300), (0,0)]
        #idle or not
        self.idle = False
    def __repr__(self):
        return self.pos.__repr__()
        
    def __str__(self):
        return self.__repr__()

    def walk_random(self):
        '''walks random.. but looks more like vibrating'''
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        self.change_direction(dx, dy)
        for x in range(0, randint(5,10)):
            print x
            self.move(dx, dy)
    
    def set_random_goal(self):
        '''set random goal within 100 pixels around itself, looks a lot better than walk_random'''
        randomx = randint(-100, 100)
        randomy = randint(-100, 100)
        new_x = self.pos[0] + randomx
        new_y = self.pos[1] + randomy
        new_x, new_y = self.boundcheck(new_x, new_y)
        self.goal = (new_x, new_y)

        
    def walk_to_place(self, level, goal):
        '''walk to goal  in straight line, depending on self.speed'''
        DX = self.pos[0] - goal[0]
        DY = self.pos[1] - goal[1]
        total_length = (DX**2 + DY**2)**0.5
        dx = -1*self.speed/total_length * DX
        dy = -1*self.speed/total_length * DY
        self.change_direction(dx, dy)
        self.collision_move(level,dx, dy)

    def walk_away_from_place(self, level, goal):
        '''walk away from place in straight line, depending on self.speed'''
        DX = self.pos[0] - goal[0]
        DY = self.pos[1] - goal[1]
        total_length = (DX**2 + DY**2)**0.5
        dx = self.speed/total_length * DX
        dy = self.speed/total_length * DY
        self.change_direction(dx, dy)
        self.collision_move(level,dx, dy)
        
    def change_direction(self, dx, dy):
        ''' change self.direction depending on .., well, direction!'''
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
                
    def __repr__(self):
        return self.pos.__repr__()
       
    def __str__(self):
        return self.__repr__()
    
    def distance(self, pos1, pos2):
        '''returns distance of 2 positions'''
        DX = pos1[0] - pos2[0]
        DY = pos1[1] - pos2[1]
        total_length = (DX**2 + DY**2)**0.5
        return total_length
        
    def get_goal_from_path(self):
        '''gets goal from self.path, removes entry from path when it is entered as goal'''
        if self.goal == None and self.path:
            self.goal = self.path[0] 
            self.path.remove(self.path[0])
        elif self.goal is not None and abs(self.distance(self.pos, self.goal)) < 3:
            if self.path:
                self.goal = self.path[0]
                self.path.remove(self.path[0])
            else:
                self.goal = None
                self.path = None
                
                
    def boundcheck(self, x, y):
        '''checks if x and y are within screen bounds ( hardcoded for now)'''
        x = x if x > 0 else 0
        x = x if x < 1120 else 1120 -10
        y = y if y > 0 else 0
        y = y if y < 320 else 320 -10
        return x, y
        
    def update(self, level):
        if self.distance(self.pos, level.player.pos) < 100:
            self.walk_away_from_place(level, level.player.pos)
        elif not self.idle:
            if self.animation is None:
                self.animation = self.walk_animation()
            self.get_goal_from_path()
            if self.goal is not None:
                self.walk_to_place(level,self.goal)
            else:
                self.set_random_goal()
                   
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
        self.animation = None
      
    def update(self, level,*args): # TODO use/remove *args
        """Run the current animation or just stand there if no animation set."""
        if self.animation is None:
            self.image = self.frames[self.direction][0]
        else:
            try:
                if self.animation_speed_check():
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
