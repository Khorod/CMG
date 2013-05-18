"""By Michael Cabot, Steven Laan, Richard Rozeboom"""
import pygame
import astar
import ConfigParser
from utils import Point

COLLISION_MAP = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

MAP_TILE_WIDTH = 24
MAP_TILE_HEIGHT = 16

class World:
    """Word class"""

    def __init__(self, collision_map, flow_map, mesh):
        self.collision_map = collision_map
        self.flow_map = flow_map
        self.mesh = mesh
        self.height = 10
        self.width  = 10
        self.tilesize = 40

    def plan_path(self, start, goal):
        """Return optimal path from start to goal."""
        goal_func = lambda x: x == goal
        heur_func = lambda x: goal.dist(x)
        cost_func = lambda x, y: 1

        path, _ = astar.astar(start, self.neighbors, goal_func, 0, 
            cost_func, heur_func)
        return path

    def neighbors(self, pos, wall = 1):
        """Yield the neighbouring positions."""
        if pos.x > 0:
            if self.collision_map[pos.x - 1][pos.y] < wall:
                yield pos - (1, 0)

        if pos.x < self.width - 1:
            if self.collision_map[pos.x + 1][pos.y] < wall:
                yield pos + (1, 0)
        
        if pos.y > 0:
            if self.collision_map[pos.x][pos.y - 1] < wall:
                yield pos - (0, 1)

        if pos.y < self.height - 1:
            if self.collision_map[pos.x][pos.y + 1] < wall:
                yield pos + (0, 1)
    
    def place_free(self, game_object, pos):
        """"Checks whether a place is collision-free. 
        Position is in pixel coordinates.
        Place is determined using the shape of the game object"""

        # TODO implement
        return True

    def position_free(self, pos):
        """Checks whether a position is collision-free.
        Position is in pixel coordinates."""

        # TODO implement
        return True

    def __repr__(self):
        pass

    def __str__(self):
        pass

class TileCache:
    """Load the tilesets lazily into global cache"""

    def __init__(self,  width=32, height=None):
        self.width = width
        self.height = height or width
        self.cache = {}

    def __getitem__(self, filename):
        """Return a table of tiles, load it from disk if needed."""

        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width,
                                               self.height)
            self.cache[key] = tile_table
            return tile_table

    def _load_tile_table(self, filename, width, height):
        """Load an image and split it into tiles."""

        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width/width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table

MAP_CACHE = TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)

class Level(object):

        
    def load_file(self, filename="level.map"):
        self.map = []
        self.key = {}
                    
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)
        
        self.items = {}
        for y, line in enumerate(self.map):
            for x, c in enumerate(line):
                if not self.is_wall(x, y) and 'sprite' in self.key[c]:
                    self.items[(x, y)] = self.key[c]

    def get_tile(self, x, y):
        """Tell what's at the specified position of the map."""

        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def is_wall(self, x, y):
        """Is there a wall?"""

        return self.get_bool(x, y, 'wall')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')


    def render(self):
        wall = self.is_wall
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width*MAP_TILE_WIDTH, 
            self.height*MAP_TILE_HEIGHT))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if wall(map_x, map_y):
                    # Draw different tiles depending on neighbourhood
                    if not wall(map_x, map_y+1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            tile = 1, 2
                        elif wall(map_x+1, map_y):
                            tile = 0, 2
                        elif wall(map_x-1, map_y):
                            tile = 2, 2
                        else:
                            tile = 3, 2
                    else:
                        if wall(map_x+1, map_y+1) and wall(map_x-1, map_y+1):
                            tile = 1, 1
                        elif wall(map_x+1, map_y+1):
                            tile = 0, 1
                        elif wall(map_x-1, map_y+1):
                            tile = 2, 1
                        else:
                            tile = 3, 1
                    # Add overlays if the wall may be obscuring something
                    if not wall(map_x, map_y-1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            over = 1, 0
                        elif wall(map_x+1, map_y):
                            over = 0, 0
                        elif wall(map_x-1, map_y):
                            over = 2, 0
                        else:
                            over = 3, 0
                        overlays[(map_x, map_y)] = tiles[over[0]][over[1]]
                else:
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 0, 3
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
        return image, overlays       
if __name__ == '__main__':
    WORLD = World(COLLISION_MAP, None, None)
    print WORLD.plan_path(Point(1, 1), Point(6, 4))

