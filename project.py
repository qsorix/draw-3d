from objects import S, Wall
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

    plane_normal = funcs.Vector(1.12, 2.23, 3.34)

    vector_on_the_plane = funcs.Vector(plane_normal.z,
                                       plane_normal.x,
                                       plane_normal.y)

    def nodes_angle(node):
        projected = funcs.vector_plane_projection(
            funcs.vector_from_to(parent.point, node.point),
            funcs.Plane(plane_normal, parent))

        x = funcs.vector_vector_projection(projected, vector_on_the_plane)
        y = funcs.sub_vectors(projected, x)
        # in x and y only one direction is non-zero, but i don't know which, so
        # i sum them up...
        return math.atan2(x.x+x.y+x.z,
                          y.x+y.y+y.z)

    return sorted(nodes, key=nodes_angle)

class Backtrack(Exception):
    def __init__(self, node):
        self.node = node

def _dfs_fcp_impl(node, plane_normal, cycle, results):
    for nbr in clockwise_sorted(node, node.neighbors, plane_normal):
        if nbr == cycle[-2]:
            continue

        if nbr == cycle[0]:
            return True

        if nbr in cycle:
            raise Backtrack(nbr)

        normal = None
        if len(cycle) >= 2:
            same_plane, normal = _vertexes_are_on_the_same_plane(cycle[-2],
                                                                 cycle[-1], nbr,
                                                                 plane_normal)

            if not same_plane:
                continue

        cycle.append(nbr)
        try:
            found = _dfs_fcp_impl(nbr, normal, cycle, results)
            if found:
                results.append(cycle.copy())
                if plane_normal:
                    return True
        except Backtrack as btr:
            if btr.node != nbr:
                cycle.pop()
                raise
        cycle.pop()

    return False

def _dfs_find_cycle_on_plane(va, vb):
    cycle = [va, vb]
    results = []
    try:
        _dfs_fcp_impl(vb, None, cycle, results)
    except Backtrack:
        pass
    return results

class Vertex:
    def __init__(self, point):
        self.point = point
        self.neighbors = set()
        self.dfs_mark = 0

    def __repr__(self):
        return "Vertex{}".format(self.point)

    def add_neighbor(self, neighbor):
        if self == neighbor:
            return

        for n in self.neighbors:
            if n == neighbor:
                return
        self.neighbors.add(neighbor)

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
            break

    def _split_segment(self, segment, vertex):
        """split segment by adding a vertex in the middle"""
        va = self.get_vertex(segment.a)
        vb = self.get_vertex(segment.b)

        self.add_neighborhood(va, vertex)
        self.add_neighborhood(vb, vertex)
        va.neighbors.discard(vb)
        vb.neighbors.discard(va)

    def add_segment(self, segment):
        print("add segment", segment)
        va = self.add_vertex(segment.a)
        vb = self.add_vertex(segment.b)
        vb_final = vb

        segments_to_remove = []
        segments_to_add = []

        def add_and_remove():
            for sr in segments_to_remove:
                for se in self.segments:
                    if se.equals_ignoring_direction(sr):
                        self.segments.remove(se)
                        break
            self.segments.extend(segments_to_add)

        for s in self.segments:
            if s == segment:
                continue

            intersection = funcs.segment_segment_intersection(s, segment)
            if intersection:
                iv = self.add_vertex(intersection)
                if iv.point != va.point:
                    vb_final = iv

                #print (s, " and ", segment, " intersect at ", intersection)
                #print ("s.a: ", s.a)
                #print ("s.b: ", s.b)
                #print ("seg.a: ", segment.a)
                #print ("seg.b: ", segment.b)

                if ((intersection == s.a or
                     intersection == s.b) and
                    (intersection == segment.a or
                     intersection == segment.b)):
                    continue

                if (intersection != s.a and
                    intersection != s.b):
                    self._split_segment(s, iv)
                    segments_to_add.append(S(s.a, intersection))
                    segments_to_add.append(S(intersection, s.b))
                    segments_to_remove.append(s)

                if (intersection != segment.a and
                    intersection != segment.b):
                    add_and_remove()
                    self.add_segment(S(segment.a, iv.point))
                    self.add_segment(S(iv.point, segment.b))
                    return

        add_and_remove()

        print("appending ", segment)
        self.segments.append(segment)
        self.add_neighborhood(va, vb)

        #self.try_spawning_walls(va, vb_final)

    def _try_simplifying_vertex(self, v):
        if not v.neighbors:
            self.vertices.remove(v)

        elif len(v.neighbors) == 2:
            # if both neighbors for a straight line through this vertex, we can
            # remove it to simplify the model
            v1, v2 = list(v.neighbors)
            a = funcs.vector_from_to(v1.point,
                                     v.point)
            b = funcs.vector_from_to(v.point,
                                     v2.point)

            if funcs.cross(a, b).is_zero():
                v1.neighbors.remove(v)
                v2.neighbors.remove(v)
                self._del_segment_from_list(S(v1.point, v.point))
                self._del_segment_from_list(S(v.point, v2.point))
                self.add_segment(S(v1.point, v2.point))
                self.vertices.remove(v)

    def _del_segment_from_list(self, segment):
        for s in self.segments:
            if s.equals_ignoring_direction(segment):
                self.segments.remove(s)
                return True
        return False

    def del_segment(self, segment):
        if not self._del_segment_from_list(segment):
            return

        va = self.get_vertex(segment.a)
        vb = self.get_vertex(segment.b)
        print (va, va.neighbors)
        print (vb, vb.neighbors)
        if vb in va.neighbors:
            va.neighbors.remove(vb)
        if va in vb.neighbors:
            vb.neighbors.remove(va)

        self._try_simplifying_vertex(va)
        self._try_simplifying_vertex(vb)
