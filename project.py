from objects import Wall

def dfs_find_cycle(v, parent):
    v.dfs_mark = 1
    for n in v.neighbors:
        if n == parent:
            continue

        if n.dfs_mark != 0:
            return [v]

        res = dfs_find_cycle(n, v)
        if res:
            res.append(v)
            return res

    v.dfs_mark = 2

class Vertex:
    def __init__(self, point):
        self.point = point
        self.neighbors = []
        self.dfs_mark = 0

    def __repr__(self):
        return "Vertex{}".format(self.point)

    def add_neighbor(self, neighbor):
        if self == neighbor:
            return

        for n in self.neighbors:
            if n == neighbor:
                return
        self.neighbors.append(neighbor)

class Project:
    def __init__(self):
        self.segments = []
        self.walls = []
        self.vertices = []

    def add_vertex(self, point):
        vertex = self.get_vertex(point)
        if not vertex:
            vertex = Vertex(point)
            self.vertices.append(vertex)
        return vertex

    def get_vertex(self, point):
        for v in self.vertices:
            if point == v.point:
                return v

    def add_neighborhood(self, v1, v2):
        v1.add_neighbor(v2)
        v2.add_neighbor(v1)

    def create_wall_from_cycle(self, cycle):
        points = []
        for v in cycle:
            points.append(v.point)
        self.walls.append(Wall(points))

    def try_spawning_walls(self, v):
        for v in self.vertices:
            v.dfs_mark = 0

        cycle = dfs_find_cycle(v, v)
        if cycle:
            self.create_wall_from_cycle(cycle)

    def add_segment(self, segment):
        self.segments.append(segment)
        va = self.add_vertex(segment.a)
        vb = self.add_vertex(segment.b)

        self.add_neighborhood(va, vb)

        self.try_spawning_walls(va)
