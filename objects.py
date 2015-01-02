from colors import *
import funcs
from funcs import vector_from_to

class S:
    def __init__(self, start, end, color = black):
        if not start:
            raise Exception("Segment requires start")
        if not end:
            raise Exception("Segment requires end")
        self.a = start
        self.b = end
        self.color = color
        self.active = False

    def __repr__(self):
        return "S({0}, {1})".format(self.a, self.b)

    def vertices_iter(self):
        yield self.a
        yield self.b

    def equals_ignoring_direction(self, other):
        return ((self.a == other.a and self.b == other.b) or
                (self.a == other.b and self.b == other.a))

class Wall:
    def __init__(self, vertices):
        if len(vertices) < 3:
            raise Exception("Wall needs at least 3 sides")
        self.vertices = vertices
        self.active = False

    def plane(self):
        return funcs.Plane(self.normal(), self.vertices[0])

    def normal(self):
        v1 = vector_from_to(self.vertices[0],
                            self.vertices[1])
        for i in range(2, len(self.vertices)):
            v2 = vector_from_to(self.vertices[i-1],
                                self.vertices[i])

            n = funcs.cross(v1, v2)
            if n and not n.is_zero():
                return n

        raise Exception("Failed to calculate normal to a wall")

    def vertices_iter(self):
        return self.vertices
