"""By Michael Cabot, Steven Laan, Richard Rozeboom"""
import astar
import math
import copy

# Shortcuts
sqrt  = math.sqrt
try:
    inf = float('inf')
except ValueError:
    inf = 1e1000000
pi    = math.pi
astar = astar.astar

class Point(tuple):
    """Point object expands 'tuple' with arithmetic operators:
    >>> Point(4, 5) + Point(6, 5)
    Point(10, 10)

    Operations also work together with tuples!
    >>> Point(4, 5) + (1, 2)
    Point(5, 7)

    Although it is a subclass of tuple, you can refer to coords:
    >>> p = Point(4, 5)
    >>> p.x
    4

    Awesome!"""

    def __new__(cls, a, b):
        return super(Point, cls).__new__(cls, tuple((a, b)))

    def __init__(self, x, y):
        super(Point, self).__init__(x, y)

    def __isub__(self, other):
        if isinstance(other, Point) or isinstance(other, tuple):
            self = Point(self[0] - other[0], self[1] - other[1])
            return self
        else:
            raise NotImplementedError()

    def __sub__(self, other):
        if isinstance(other, Point) or isinstance(other, tuple):
            return Point(self[0] - other[0], self[1] - other[1])
        else:
            raise NotImplementedError()

    def __iadd__(self, other):
        if isinstance(other, Point) or isinstance(other, tuple):
            self = Point(self[0] + other[0], self[1] + other[1])
            return self
        else:
            raise NotImplementedError()

    def __add__(self, other):
        if isinstance(other, Point) or isinstance(other, tuple):
            return Point(self[0] + other[0], self[1] + other[1])
        else:
            raise NotImplementedError()

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Point(self[0] * other, self[1] * other)
        else:
            raise NotImplementedError()

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self = Point(self[0] * other, self[1] * other)
            return self
        else:
            raise NotImplementedError()

    def __getattribute__(self, name):
        if name == 'x':
            return self[0]
        elif name == 'y':
            return self[1]
        else:
            return object.__getattribute__(self, name)

    def __eq__(self, other):
        if isinstance(other, Point) or isinstance(other, tuple):
            return self[0] == other[0] and self[1] == other[1]
        else:
            raise NotImplementedError()

    def dist(self, other):
        if isinstance(other, Point) or isinstance(other, tuple):
            diff = self - other
            return (diff[0]**2 + diff[1]**2)**0.5
        else:
            return NotImplementedError()

    def dot(self, other):
        if isinstance(other, Point) or isinstance(other, tuple):
            return Point(self.x * other[0], self.y * other[1])
        else:
            return NotImplementedError()

    def __repr__(self):
        return 'Point(%s, %s)' % (self.x, self.y)

    def __str__(self):
        return self.__repr__()

def point_dist(a, b):
    """ Distance between two points. """
    return ((a[0]-b[0]) ** 2 + (a[1]-b[1]) ** 2) ** 0.5

def line_intersects_rect(p0, p1, r):
    """ Check where a line between p1 and p2 intersects
        given axis-aligned rectangle r.
        Returns False if no intersection found.
        Uses the Liang-Barsky line clipping algorithm.

        >>> line_intersects_rect((1.0,0.0),(1.0,4.0),(0.0,1.0,4.0,1.0))
        ((0.25, (1.0, 1.0)), (0.5, (1.0, 2.0)))

        >>> line_intersects_rect((1.0,0.0),(3.0,0.0),(0.0,1.0,3.0,1.0))
        False
    """
    l,t,r,b = (r[0],r[1],r[0]+r[2],r[1]+r[3])
    p0x,p0y = p0
    q0x,q0y = p1
    t0,t1  = 0.0, 1.0
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    for edge in xrange(4):
        if edge == 0:
            p,q = -dx, -(l-p0x)
        elif edge == 1:
            p,q = dx, (r-p0x)
        elif edge == 2:
            p,q = -dy, -(t-p0y)
        else:
            p,q = dy, (b-p0y)
        if p == 0: # Parallel line
            if q < 0:
                return False
        else:
            ti = q/float(p)
            if p < 0:
                if ti > t1:
                    return False
                elif ti > t0:
                    t0 = ti
            else:
                if ti < t0:
                    return False
                elif ti < t1:
                    t1 = ti
    # Return (two) intersection coords
    return ((t0, (p0x + t0*dx, p0y + t0*dy)), (t1, (p0x + t1*dx, p0y + t1*dy)))
    
def line_intersects_rects(p0, p1, rects):
    print p0, p1, rects
    if rects:
        for rect in rects:
            if line_intersects_rect(p0, p1, rect):
                return True
    return False

def line_intersects_grid((x0,y0), (x1,y1), grid, grid_cell_size=(1,1)):
    """ Performs a line/grid intersection, finding the "super cover"
        of a line and seeing if any of the grid cells are occupied.
        The line runs between (x0,y0) and (x1,y1), and (0,0) is the
        top-left corner of the top-left grid cell.

        >>> line_intersects_grid((0,0),(2,2),[[0,0,0],[0,1,0],[0,0,0]])
        True

        >>> line_intersects_grid((0,0),(0.99,2),[[0,0,0],[0,1,0],[0,0,0]])
        False
    """
    grid_cell_width = float(grid_cell_size[0])
    grid_cell_height = float(grid_cell_size[1])
    x0 = x0 / grid_cell_width
    x1 = x1 / grid_cell_width
    y0 = y0 / grid_cell_height
    y1 = y1 / grid_cell_height
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x = int(math.floor(x0))
    y = int(math.floor(y0))
    if dx != 0:
        dt_dx = 1.0 / dx
    else:
        dt_dx = inf
    if dy != 0:
        dt_dy = 1.0 / dy
    else:
        dt_dy = inf
    t = 0.0
    n = 1
    if (dx == 0):
        x_inc = 0
        t_next_horizontal = dt_dx
    elif (x1 > x0):
        x_inc = 1
        n += int(math.floor(x1)) - x
        t_next_horizontal = (math.floor(x0) + 1 - x0) * dt_dx
    else:
        x_inc = -1
        n += x - int(math.floor(x1))
        t_next_horizontal = (x0 - math.floor(x0)) * dt_dx
    if (dy == 0):
        y_inc = 0
        t_next_vertical = dt_dy
    elif (y1 > y0):
        y_inc = 1
        n += int(math.floor(y1)) - y
        t_next_vertical = (math.floor(y0) + 1 - y0) * dt_dy
    else:
        y_inc = -1
        n += y - int(math.floor(y1))
        t_next_vertical = (y0 - math.floor(y0)) * dt_dy
    while (n > 0):
        if grid[y][x] == 1:
            return True
        if (t_next_vertical < t_next_horizontal):
            y += y_inc
            t = t_next_vertical
            t_next_vertical += dt_dy
        else:
            x += x_inc
            t = t_next_horizontal
            t_next_horizontal += dt_dx
        n -= 1
    return False

def rect_contains_point(rect, point):
    """ Check if rectangle contains a point. """
    if (rect[0] <= point[0] and
        rect[1] <= point[1] and
        rect[0] + rect[2] >= point[0] and
        rect[1] + rect[3] >= point[1]):
        return True
    return False

def rect_offset(rect, offset):
    """ Offsets (grows) a rectangle in each direction. """
    return (rect[0] - offset, rect[1] - offset, rect[2]+2*offset, rect[3]+2*offset)

def rect_corners(rect):
    """ Returns cornerpoints of given rectangle.

        >>> rect_corners((1,2,1,3))
        ((1, 2), (2, 2), (2, 5), (1, 5))
    """
    tl = (rect[0],rect[1])
    tr = (rect[0]+rect[2],rect[1])
    br = (rect[0]+rect[2],rect[1]+rect[3])
    bl = (rect[0],rect[1]+rect[3])
    return (tl,tr,br,bl)

def rects_bound(rects):
    """ Returns a rectangle that bounds all given rectangles

        >>> rects_bound([(0,0,1,1), (3,3,1,1)])
        (0, 0, 4, 4)
    """
    def rb((ax,ay,aw,ah), (bx,by,bw,bh)):
        x = min(ax, bx)
        y = min(ay, by)
        w = max(ax+aw, bx+bw) - x
        h = max(ay+ah, by+bh) - y
        return (x,y,w,h)
    return reduce(rb, rects)

def rects_merge(rects):
    """ Merge a list of rectangle (xywh) tuples.
        Returns a list of rectangles that cover the same
        surface. This is not necessarily optimal though.

        >>> rects_merge([(0,0,1,1),(1,0,1,1)])
        [(0, 0, 2, 1)]
    """
    def stack(rects, horizontal=False):
        """ Stacks rectangles that connect in either horizontal
            or vertical direction.
        """
        if horizontal:
            rects = [(y,x,h,w) for (x,y,w,h) in rects]
        rects.sort()
        newrects = []
        i = 0
        while i < len(rects):
            (x1,y1,w1,h1) = rects[i]
            # Initialize new rect to this one
            nr = [x1,y1,w1,h1]
            # While the next rectangle connects to this one:
            while (i+1 < len(rects) and
                    nr[0] == rects[i+1][0] and
                    nr[2] == rects[i+1][2] and
                    nr[1]+nr[3] == rects[i+1][1]):
                # Increase height of the current new rect
                nr[3] += rects[i+1][3]
                i += 1
            i += 1
            newrects.append(tuple(nr))
        # Flip rects back if we were stacking horizontally
        if horizontal:
            newrects = [(x,y,w,h) for (y,x,h,w) in newrects]
        return newrects
    # Stack twice, once in each direction
    return stack(stack(rects),horizontal=True)

def make_nav_mesh(walls, bounds=None, offset=7, simplify=0.0001, add_points=[]):
    """ Generate an almost optimal navigation mesh
        between the given walls (rectangles), within
        the world bounds (a big rectangle).
        Mesh is a dictionary of dictionaries:
            mesh[point1][point2] = distance
    """
    # If bounds not given, assume outer walls are bounds.
    if bounds is None:
        bounds = rects_bound(walls)
    # 1) Offset walls and add nodes on corners
    walls = [rect_offset(w,offset) for w in walls]
    nodes = set(add_points)
    for w in walls:
        for point in rect_corners(w):
    # 2) Remove points that are inside of other walls (or outside bounds)
            other_walls = filter(lambda x: x!=w,walls)
            if (rect_contains_point(bounds, point) and
                not any(rect_contains_point(ow, point) for ow in other_walls)):
                nodes.add((int(point[0]),int(point[1])))
    # 3) Connect nodes that can "see" eachother
    walls = [rect_offset(w,-0.001) for w in walls]
    mesh = dict((n,{}) for n in nodes)
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2:
                if not any(line_intersects_rect(n1,n2,w) for w in walls):
                    mesh[n1][n2] = point_dist(n1,n2)
    # 4) Remove direct connections that are not much shorter than indirect ones
    def astar_path_length(m, start, end):
        """ Length of a path from start to end """
        neighbours = lambda n: m[n].keys()
        cost       = lambda n1, n2: m[n1][n2]
        goal       = lambda n: n == end
        heuristic  = lambda n: point_dist(end, n)
        nodes, length = astar(start, neighbours, goal, 0, cost, heuristic)
        return length
    connections = []
    for n1 in mesh:
        for n2 in mesh[n1]:
            connections.append((mesh[n1][n2],(n1,n2)))
    connections.sort(reverse=True) # Start with the longest connections
    for length, (n1, n2) in connections:
        mesh[n1].pop(n2) # Remove connection to see best path without it
        alternative_dist = astar_path_length(mesh, n1,n2)
        # Put the connection back if the alternative is much worse
        if alternative_dist > (1+simplify) * length:
            mesh[n1][n2] = length

    return mesh

def find_path(start, end, mesh, grid, tilesize=(16,16)):
    """ Uses astar to find a path from start to end,
        using the given mesh and tile grid.

        >>> grid = [[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        >>> mesh = make_nav_mesh([(2,2,1,1)],(0,0,4,4),1)
        >>> find_path((0,0),(4,4),mesh,grid,(1,1))
        [(4, 1), (4, 4)]
    """
    # If there is a straight line, just return the end point
    if not line_intersects_grid(start, end, grid, tilesize):
        return [end]
    # Copy mesh so we can add temp nodes
    mesh = copy.deepcopy(mesh)
    # Add temp notes for start
    mesh[start] = dict([(n, point_dist(start,n)) for n in mesh if not line_intersects_grid(start,n,grid,tilesize)])
    # Add temp nodes for end:
    if end not in mesh:
        endconns = [(n, point_dist(end,n)) for n in mesh if not line_intersects_grid(end,n,grid,tilesize)]
        for n, dst in endconns:
            mesh[n][end] = dst

    neighbours = lambda n: mesh[n].keys()
    cost       = lambda n1, n2: mesh[n1][n2]
    goal       = lambda n: n == end
    heuristic  = lambda n: ((n[0]-end[0]) ** 2 + (n[1]-end[1]) ** 2) ** 0.5
    nodes, length = astar(start, neighbours, goal, 0, cost, heuristic)
    return nodes
    
def rot_vector(vector, angle):
    x = vector[0]
    y = vector[1]
    angle = math.radians(angle)
    newx = x * math.cos(angle) - y * math.sin(angle)
    newy = x * math.sin(angle) + y * math.cos(angle)
    return newx, newy

if __name__ == '__main__':
    import doctest
    doctest.testmod()
