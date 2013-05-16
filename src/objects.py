import pygame

# Own imports
import utils

class GameObject(object):
    """Abstract superclass for all objects in the game."""
    world = None

    def draw(self, surface):
        """Draws the object to the given surface."""
        raise NotImplementedError()

    def step(self):
        """Executes the main logic of the object. This method is called every timestep."""
        raise NotImplementedError()

class Person(GameObject):
    """Class for one person."""

    def __init__(self, x, y):
        GameObject.__init__(self)
        self.pos = utils.Point(x, y)
        self.goal = None
        
    def __repr__(self):
        return self.pos.__repr__()
        
    def __str__(self):
        return self.__repr__()

    def draw(self, surface):
        pygame.draw.circle(surface, (255,0,0), self.pos.tuple(), 8, 0)

    def step(self):
        pass
        
class Player(Person):
    """Player object."""

    def __init__(self, x, y):
        Person.__init__(self, x, y)
        
    def step(self):
        # Logic here!
        pass
