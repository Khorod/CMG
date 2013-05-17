"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
from random import randint

# Own imports
import utils

class GameObject(pygame.sprite.Sprite):
    """Abstract superclass for all objects in the game."""
    world = None
    def __init__(self, position, frames=None):
            super(GameObject, self).__init__()
            self.image = frames[0][0]
            self.rect = self.image.get_rect()
            self.pos = utils.Point(position[0], position[1])
        
    @property
    def _tile_pos(self):
        return utils.Point(self.pos.x / 24, self.pos.y / 16)
        
    def _get_pos(self):
        """Check the current position of the sprite on the map."""

        # TODO replace hardcoded 12 and 16
        return utils.Point((self.rect.midbottom[0]-12), (self.rect.midbottom[1]-16))

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""

        # TODO replace hardcoded 24 and 16
        self.rect.midbottom = pos.x + 12, pos.y + 16
        self.depth = self.rect.midbottom[1]

    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]        

class Person(GameObject):
    """Class for one person."""

    def __init__(self, position, image, color = None, radius = 8):
        GameObject.__init__(self, position, image)
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

    def __init__(self, position, image):
        Person.__init__(self, position, image, (255, 0, 0))
        
    def update(self):
        # Logic here!
        pass


class Cop(Person):
    """Cop object."""

    def __init__(self, pos, image):
        Person.__init__(self, pos, image, (0, 0, 255))
        
    def update(self):
        # Logic here!
        pass
