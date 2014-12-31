from objects import Wall
import funcs

def _vertexes_are_on_the_same_plane(v1, v2, v3, plane_normal):
    """Check 3 points agains a given plane. Since it is used in DFS, we only
    care about true negatives. Initially some inputs are None and this is
    normal, DFS should continue so it returns True."""

    if not v1 or not v2 or not v3:
        return True, plane_normal

    vector1 = funcs.vector_from_to(v1.point, v2.point)
    vector2 = funcs.vector_from_to(v2.point, v3.point)

    normal = funcs.unit(funcs.cross(vector1, vector2))
    if normal.is_zero():
        # points lie on the same line, so they do belong to a single plane, so
        # let's continue
        return True, plane_normal

    if not plane_normal:
        return True, normal

    #print ("Plane_normal: ", plane_normal)
    #print ("Normal:       ", normal)
    return (plane_normal == normal), plane_normal

def _dfs_find_cycle_on_plane(v, parent, plane_normal):
    res = []
    all_visited = True

    v.dfs_mark = 1
    for n in v.neighbors:
        if n == parent:
            continue
        if n.dfs_mark == 2:
            continue

        same_plane, normal = \
            _vertexes_are_on_the_same_plane(parent, v, n, plane_normal)
        if not same_plane:
            all_visited = False
            continue

        if plane_normal and n.dfs_mark != 0:
            res.append([v])
            continue

        if not plane_normal:
            plane_normal = normal

        sub_res = _dfs_find_cycle_on_plane(n, v, plane_normal)
        for sr in sub_res:
            sr.append(v)
            res.append(sr)

    if all_visited:
        v.dfs_mark = 2
    return res

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

    def try_spawning_walls(self, v_start):
        for v in self.vertices:
            v.dfs_mark = 0

        cycles = _dfs_find_cycle_on_plane(v_start, None, None)
        for cycle in cycles:
            self.create_wall_from_cycle(cycle)

    def add_segment(self, segment):
        for s in self.segments:
            intersection = funcs.segment_segment_intersection(s.a, s.b,
                                                              segment.a,
                                                              segment.b)
            if intersection:
                v = self.add_vertex(intersection)
                v1 = self.get_vertex(s.a)
                v2 = self.get_vertex(s.b)
                v3 = self.add_vertex(segment.a)
                v4 = self.add_vertex(segment.b)
                self.add_neighborhood(v, v1)
                self.add_neighborhood(v, v2)
                self.add_neighborhood(v, v3)
                self.add_neighborhood(v, v4)

        self.segments.append(segment)
        va = self.add_vertex(segment.a)
        vb = self.add_vertex(segment.b)

        self.add_neighborhood(va, vb)

        self.try_spawning_walls(va)
