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

class Wall:
    def __init__(self, vertices):
        self.vertices = vertices
        self.active = False

    def plane(self):
        return funcs.Plane(self.normal(), self.vertices[0])

    def normal(self):
        res = funcs.cross(vector_from_to(self.vertices[0],
                                         self.vertices[1]),
                          vector_from_to(self.vertices[1],
                                         self.vertices[2]))
        if not res or not funcs.length(res):
            raise Exception("Failed to calculate normal to a wall")

        return res
