"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import astar
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

    def __repr__(self):
        pass

    def __str__(self):
        pass

if __name__ == '__main__':
    WORLD = World(COLLISION_MAP, None, None)
    print WORLD.plan_path(Point(1, 1), Point(6, 4))

