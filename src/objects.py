"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
from random import randint
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

    def update(self, *args):
            """Run the current animation."""
            self.animation.next()                

class Person(GameObject):
    """Class for one person."""

    def __init__(self, position, image, color = None, rect = None, radius = 8):
        GameObject.__init__(self, position, image, rect)
        self.goal = None
        if color != None:
            self.color = color
        else:
            self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.radius = radius
        
    def __repr__(self):
        return self.pos.__repr__()
        
    def __str__(self):
        return self.__repr__()

    def update(self):
        pass


class Player(Person):
    """Player object."""

    def __init__(self, position, image, rect = None, radius = 8):
        Person.__init__(self, position, image, (255, 0, 0), rect, radius)
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
            
    def update(self, *args):
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

    def __init__(self, pos, image):
        Person.__init__(self, pos, image, (0, 0, 255))
        
    def update(self):
        # Logic here!
        pass
