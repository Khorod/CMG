class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __isub__(self, other):
        if isinstance(other, Point):
            self.x -= other.x
            self.y -= other.y
            return self
        elif isinstance(other, tuple):
            self.x -= other[0]
            self.y -= other[1]
            return self
        else:
            raise NotImplementedError()

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Point(self.x - other[0], self.y - other[1])
        else:
            raise NotImplementedError()

    def __iadd__(self, other):
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            return self
        elif isinstance(other, tuple):
            self.x += other[0]
            self.y += other[1]
            return self
        else:
            raise NotImplementedError()

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        else:
            raise NotImplementedError()

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x * other, self.y * other)
        else:
            raise NotImplementedError()

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
        else:
            raise NotImplementedError()

    def __str__(self):
        return 'Point %f %f' % (self.x, self.y)

    def tuple(self):
        return (self.x, self.y)
