class Point(tuple):

    def __new__(cls, a, b):
        return super(Point, cls).__new__(cls, tuple((a,b)))

    def __init__(self, x, y):
        super(Point, self).__init__(x,y)

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
if __name__ == '__main__':
    origin = Point(0,0)
    p = Point(3,4)
    p2 = Point(3,4)
    print p + p2
    print p + (1,2)
    print 'x of p:', p.x
    print hash(p), hash(p2)
