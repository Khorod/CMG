import astar


class World:

    def __init__(self, collision_map, flow_map, mesh):
        self.collision_map = collision_map
        self.flow_map = flow_map
        self.mesh = mesh

    def plan_path(self, start, goal):
        path, _ = astar.astar(start, self.neighbors, goal, 0, 
            self.cost, self.heuristic)
        return path

    def neighbors(self, pos):
        return self.mesh[pos]

    def cost(self, start, end):
        pass

    def heuristic(self, start, end):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass
