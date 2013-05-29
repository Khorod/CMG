"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
from world import MAP_TILE_WIDTH, MAP_TILE_HEIGHT

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

    def stand_animation(self):
        """The default animation."""

        while True:
            # Change to next frame every two ticks
            for frame in self.frames[0]:
                self.image = frame
                yield None
                yield None

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
        self.goal = None
        self.direction = 2
        self.animation = None
        self.image = self.frames[self.direction][0]
        #path to follow
        self.path = None#[(300,0),(500,150),(600,150)]#[(0,0), (1100,5), (1100, 300), (0, 300), (0,0)]
        #idle or not
        self.idle = False
        self.creeper_comfort_zone = 100
        self.person_comfort_zone = 2

    def update(self):
        pass

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

    def distance(self, pos1, pos2):
        '''returns distance of 2 positions'''
        DX = pos1[0] - pos2[0]
        DY = pos1[1] - pos2[1]
        total_length = (DX**2 + DY**2)**0.5
        return total_length

    def get_goal_from_path(self):
        '''gets goal from self.path, removes entry from path when it is entered as goal'''
        if not self.goal and self.path:
            self.goal = (self.path[0][0]*MAP_TILE_WIDTH , self.path[0][1]*MAP_TILE_HEIGHT)
            self.path.remove(self.path[0])
        elif self.goal is not None and abs(self.distance(self.pos, self.goal)) < 30:
            if self.path:
                self.goal = (self.path[0][0]*MAP_TILE_WIDTH , self.path[0][1]*MAP_TILE_HEIGHT)
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

    def walk_from_player(self,level):
        if self.distance(self.pos, level.player.pos) < self.creeper_comfort_zone:
            self.walk_away_from_place(level, level.player.pos)
            return True
        else:
            return False

    def walk_from_person(self, level):
        for obj in level.game_objects:
            if self is not obj:
                if self.distance(self.pos, obj.pos) < self.person_comfort_zone:
                    self.walk_away_from_place(level, obj.pos)
                    return True
        return False

    def update(self, level):
        if self.walk_from_player(level):
            pass
        elif self.walk_from_person(level):
            pass
        elif not self.idle:
            if self.animation is None:
                self.animation = self.walk_animation()
            self.get_goal_from_path()
            if self.goal is not None:
                self.walk_to_place(level,self.goal)
            else:
                pass#self.set_random_goal(level)

        #if not self.path and not self.goal:
        #self.path = level.plan_path(utils.Point(int(self.pos[0]),int(self.pos[1])), utils.Point(self.final_goal[0],self.final_goal[1]))
        if self.final_goal:
            self.path = level.plan_path(self._tile_pos, utils.Point(self.final_goal[0]/MAP_TILE_WIDTH,self.final_goal[1]/MAP_TILE_HEIGHT) )

        if self.final_goal:
            if self.distance(self.pos, self.final_goal) < 30:
                self.final_goal = None

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
        self.image = self.frames[self.direction][0]

    def walk_animation(self):
        """Animation for the player walking."""
        # This animation is hardcoded for 4 frames and 16x24 map tiles
        for frame in range(4):
            self.image = self.frames[self.direction][frame]
            '''yield None
            yield None
            yield None
            yield None
            yield None
            yield None'''

    def update(self, *args): # TODO use/remove *args
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

    def update(self):
        # Logic here!
        pass
