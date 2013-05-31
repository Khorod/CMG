"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
from world import MAP_TILE_WIDTH, MAP_TILE_HEIGHT
from random import randint
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
        self.animation_speed = 8 #higher is slower

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

    pos = property(_get_pos, _set_pos) # magic

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

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__,
                               self.pos[0], self.pos[1])

    def __str__(self):
        return self.__repr__()

class Person(GameObject):
    """Class for one person."""
    def __init__(self, position, image, rect):
        GameObject.__init__(self, position, image, rect)
        self.final_goal = (40, 128)
        self.goal = None
        self.direction = 2
        self.animation = None
        self.image = self.frames[self.direction][0]
        self.path = None
        self.idle = True

    def walk_to_place(self, level, goal):
        """walk to goal in straight line, depending on self.speed"""
        DX = self.pos[0] - goal[0]
        DY = self.pos[1] - goal[1]
        total_length = (DX**2 + DY**2)**0.5
        dx = -1 * self.speed / total_length * DX
        dy = -1 * self.speed / total_length * DY
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

    def update(self, level):
        if not self.path:
            self.path = level.plan_path(self.pos, self.final_goal)
        else:
            if self.animation is None:
                self.animation = self.walk_animation()
            adjusted_pos = utils.Point( self.path[0][0], self.path[0][1]) - self._offset
            self.walk_to_place(level, adjusted_pos)

            if self.pos.dist(adjusted_pos) < self.speed:
                del self.path[0]


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

    def update(self, level):
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
