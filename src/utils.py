class Point(tuple):
    """
    A representation of a point. Also implements basic arithmetic:
    >>> Point(4, 5) + Point(6, 5)
    (10, 10)

    Operations also work together with tuples!
    >>> Point(4, 5) + (1, 2)
    (5, 7)

    Although it is a subclass of tuple, you can refer to coords:
    >>> p = Point(4, 5)
    >>> p.x
    4

    Awesome!
    """

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
    import doctest
    doctest.testmod()

