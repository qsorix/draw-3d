from objects import Wall
import funcs
import math

def _totuple(p):
    return (p.x, p.y, p.z)

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

    nc = funcs.cross(plane_normal, normal)
    return nc.is_zero(), plane_normal

def clockwise_sorted(parent, nodes, plane_normal):
    if len(nodes) <= 1:
        return nodes

    if not plane_normal:
        return nodes

    vector_on_the_plane = funcs.Vector(plane_normal.y,
                                       plane_normal.z,
                                       plane_normal.x)

    def nodes_angle(node):
        projected = funcs.vector_plane_projection(
            funcs.vector_from_to(parent.point, node.point),
            funcs.Plane(plane_normal, parent))

        x = funcs.vector_vector_projection(projected, vector_on_the_plane)
        y = funcs.sub_vectors(projected, x)
        return math.atan2(funcs.length(x),
                          funcs.length(y))

    return sorted(nodes, key=nodes_angle)

def _dfs_fcp_impl(node, plane_normal, cycle, results):
    for nbr in clockwise_sorted(node, node.neighbors, plane_normal):
        print ("> ", node, nbr, cycle)
        if nbr == cycle[-2]:
            continue

        if nbr == cycle[0]:
            print ("!", node, nbr, cycle)
            return True

        if nbr in cycle:
            return False

        normal = None
        if len(cycle) >= 2:
            same_plane, normal = _vertexes_are_on_the_same_plane(cycle[-2],
                                                                 cycle[-1], nbr,
                                                                 plane_normal)

            if not same_plane:
                continue

        cycle.append(nbr)
        print ("  ", cycle)
        found = _dfs_fcp_impl(nbr, normal, cycle, results)
        if found:
            results.append(cycle.copy())
            if plane_normal:
                return True
        cycle.pop()

    return False

def _dfs_find_cycle_on_plane(va, vb):
    cycle = [va, vb]
    results = []
    _dfs_fcp_impl(vb, funcs.Vector(0, 0, 1), cycle, results)
    return results

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

        new_points = sorted(points, key=_totuple)

        for w in self.walls:
            walls_points = sorted(w.vertices, key=_totuple)
            print (walls_points)
            if new_points == walls_points:
                # such wall exists already
                return

        print ("Adding a wall on ", points)
        self.walls.append(Wall(points))

    def try_spawning_walls(self, va, vb):
        for v in self.vertices:
            v.dfs_mark = 0

        cycles = _dfs_find_cycle_on_plane(va, vb)
        for cycle in cycles:
            self.create_wall_from_cycle(cycle)

    def add_segment(self, segment):
        for s in []:
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

        self.try_spawning_walls(va, vb)
