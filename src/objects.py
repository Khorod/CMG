"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
from random import randint

# Own imports
import utils

class GameObject(object):
    """Abstract superclass for all objects in the game."""
    world = None

    def draw(self, surface):
        """Draws the object to the given surface."""
        raise NotImplementedError()

    def step(self):
        """Executes the main logic of the object. This method is called every 
        timestep."""
        raise NotImplementedError()

class Person(GameObject):
    """Class for one person."""

    def __init__(self, x, y, color = None, radius = 8):
        GameObject.__init__(self)
        self.pos = utils.Point(x, y)
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

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, tuple(self.pos), self.radius, 0)

    def step(self):
        pass


class Player(Person):
    """Player object."""

    def __init__(self, x, y):
        Person.__init__(self, x, y, (255, 0, 0))
        
    def step(self):
        # Logic here!
        pass


class Cop(Person):
    """Cop object."""

    def __init__(self, x, y):
        Person.__init__(self, x, y, (0, 0, 255))
        
    def step(self):
        # Logic here!
        pass
