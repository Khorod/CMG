"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
from random import randint

# Own imports
import utils

class GameObject(pygame.sprite.Sprite):
    """Abstract superclass for all objects in the game."""
    world = None
    def __init__(self, position, frames, rect = None):
        super(GameObject, self).__init__()
        self.image = frames[0][0]
        if rect == None:
            self.rect = self.image.get_rect()
            print self.rect
        else:
            self.rect = rect
        self.pos = utils.Point(position[0], position[1])
        self.frames = frames
        self.animation = self.stand_animation()
        
    @property
    def _tile_pos(self):
        return utils.Point(self.pos.x / 24, self.pos.y / 16)
        
    def _get_pos(self):
        """Check the current position of the sprite on the map."""
        x, y = self.rect.center
        return utils.Point(x, y)

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
