"""By Michael Cabot, Steven Laan, Richard Rozeboom"""
import pygame
import astar
import ConfigParser
import objects
import utils

MAP_TILE_WIDTH = 32 # TODO read from ini file
MAP_TILE_HEIGHT = 16
SPRITE_WIDTH = 32
SPRITE_HEIGHT = 32

MAP_TILE_SIZE = (MAP_TILE_WIDTH, MAP_TILE_HEIGHT)

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

    def __repr__(self):
        return str(self.cache)

    def __str__(self):
        return self.__repr__()


class SortedUpdates(pygame.sprite.RenderUpdates):
    """A sprite group that sorts them by depth."""

    def sprites(self):
        """The list of sprites in the group, sorted by depth."""
        return sorted(self.spritedict.keys(), key=lambda sprite: sprite.depth)


class Level(object):

    def __init__(self, screen_size, filename="level.map"):
        self.screen_size = screen_size
        self.wall_rects = []
        self.load_file(filename)
        sprite_cache = TileCache(SPRITE_WIDTH, SPRITE_HEIGHT)
        self.game_objects = SortedUpdates()

        for tile_pos, tile in self.items.iteritems():
            position = (tile_pos[0] * MAP_TILE_WIDTH,
                        tile_pos[1] * MAP_TILE_HEIGHT)
            sprite = sprite_cache[tile["sprite"]]
            parsed_rect = [int(v) for v in tile["rect"].split(', ')]
            rect = pygame.Rect(parsed_rect)

            if tile["name"] == "player": # Create a player
                self.player = objects.Player(position, sprite, rect)
                entity = self.player
            elif tile["name"] == "person": # Create a player
                entity  = objects.Person(position, sprite, rect)
            else:
                entity = objects.GameObject(position, sprite, rect)

            self.game_objects.add(entity)

        self.wall_rects = utils.rects_merge(self.wall_rects)
        self.nav_mesh = utils.make_nav_mesh(self.wall_rects)

    def load_file(self, filename):
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
        self.grid = []
        for y, line in enumerate(self.map):
            gridline = []
            for x, c in enumerate(line):
                if self.is_wall(x, y):
                    rect = pygame.Rect(x * MAP_TILE_WIDTH, y * MAP_TILE_HEIGHT, MAP_TILE_WIDTH, MAP_TILE_HEIGHT)
                    self.wall_rects.append(rect)
                    gridline.append(1)
                else:
                    gridline.append(0)

                if 'sprite' in self.key[c]:
                    self.items[(x, y)] = self.key[c]

            self.grid.append(gridline)

    def walk_animation(self, direction):
        """Start walking in specified direction."""
        self.player.direction = direction
        self.player.animation = self.player.walk_animation()

    def move_player(self, dx, dy):
        """Move the player if this does not cause a collision. If there is a
        collision and dx and dy are both non-zero, try to move only horizontal
        or only vertical."""
        self.player.move(dx, dy)
        if not self.valid_position(self.player):
            self.player.move(-dx, 0)
            if not self.valid_position(self.player):
                self.player.move(dx, -dy)
                if not self.valid_position(self.player):
                    self.player.move(-dx, 0)


    def valid_position(self, entity):
        """Check whether the entity's position is valid, i.e. it is inside the
        screen and has no collision."""
        return not self.outside_screen(entity.pos) and \
            not self.collision(entity)

    def outside_screen(self, pos):
        """Check whether the given position is outside of the screen."""
        return pos.x < 0 or pos.y < 0 or \
            pos.x > self.screen_size[0] or pos.y > self.screen_size[1]

    def collision(self, entity):
        """Check for collision."""
        if entity.real_rect.collidelist(self.wall_rects) != -1:
            return True

        self.game_objects.remove(entity) # do not detect collision with itself
        collided = pygame.sprite.spritecollideany(entity, self.game_objects,
                                                  self.real_rect_collision)
        self.game_objects.add(entity)
        return collided

    def real_rect_collision(self, sprite1, sprite2):
        """Detect collision between the real_rect variables of the given
        sprites."""
        return pygame.Rect.colliderect(sprite1.real_rect, sprite2.real_rect)

    def update_objects(self):
        """Perform the actions of each object."""
        for obj in self.game_objects:
            obj.update(self)

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

    def is_wall(self, x, y):
        return self.get_bool(x, y, 'wall')

    def get_bool(self, x, y, name):
        """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')

    def plan_path(self, start, goal):
        """Return optimal path from start to goal."""

        path = utils.find_path(start, goal, self.nav_mesh, self.grid, MAP_TILE_SIZE)
        return path

    def render(self):
        wall = self.is_wall
        map_cache = TileCache(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)
        tiles = map_cache[self.tileset]
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

    def draw_nav_mesh(self, screen):
        # draw the nav_mesh
        for p in self.nav_mesh:
            for q in self.nav_mesh[p]:
                pygame.draw.line(screen,(0,80,0),p,q,2)

if __name__ == '__main__':
    pass

