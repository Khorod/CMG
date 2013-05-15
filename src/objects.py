import pygame

class GameObject(object):
    """Abstract superclass for all objects in the game."""

    def draw(self, surface):
        """Draws the object to the given surface."""
        raise NotImplementedError()

    def step(self):
        """Executes the main logic of the object. This method is called every timestep."""
        raise NotImplementedError()

class Person(GameObject):
    """Class for one person."""

    def __init__(self, pos):
        GameObject.__init__(self)
        self.pos = pos
        self.goal = None
        
    def __repr__(self):
        return self.pos.__repr__()
        
    def __str__(self):
        return self.__repr__()

    def draw(self, surface):
        pygame.draw.circle(surface, (255,0,0), self.pos, 20, 0)

    def step(self):
        pass
        
class Player(Person):
    """Player object."""

    def __init__(self, pos):
        Person.__init__(self, pos)
        
    def step(self):
        # Logic here!
        pass
