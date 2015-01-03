from objects import S, Wall
import funcs
import math

from arrangement import Arrangement

def arrangement_on_a_wall(proj, plane):

    arr = Arrangement(plane)

    for s in proj.segments:
        if funcs.segment_lies_on_plane(s, plane):
            arr.add_segment(s)

    print ("Found faces: ", arr.faces)

    result = []
    for f in arr.faces:
        points = []
        for v in f.hedge.cycle_vertices():
            points.append(v.point)

        w = Wall(points)

        for hole in f.inner_ccbs:
            points = []
            for v in hole.cycle_vertices():
                points.append(v.point)
            if len(points) > 2:
                w.add_hole(points)

        result.append(w)

    return result

class Vertex:
    def __init__(self, point):
        self.point = point
        self.neighbors = set()

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

    def try_spawning_walls(self, va, vb):
        planes = []
        v1 = funcs.vector_from_to(va.point, vb.point)
        for n in va.neighbors:
            v2 = funcs.vector_from_to(va.point, n.point)
            c = funcs.unit(funcs.cross(v1, v2))
            if not c.is_zero():
                found = False
                for p in planes:
                    if p.normal == c or p.normal == funcs.reverse(c):
                        found = True
                if not found:
                    planes.append(funcs.Plane(c, va.point))

        for p in planes:
            try:
                walls = arrangement_on_a_wall(self, p)

                for new_wall in walls:
                    srtd1 = sorted(new_wall.vertices, key=lambda p: (p.x, p.y, p.z))
                    found = False
                    for w in self.walls:
                        srtd2 = sorted(w.vertices, key=lambda p: (p.x, p.y, p.z))
                        if srtd1 == srtd2:
                            found = True
                            break
                    if found:
                        continue
                    else:
                        self.walls.append(new_wall)
            except AssertionError as e:
                print("AssertionError", e)
                pass

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

        if va in vb.neighbors:
            return # segment is already there

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

        self._try_simplifying_vertex(va)
        self._try_simplifying_vertex(vb)

        self.try_spawning_walls(va, vb_final)

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

                self.segments.append(S(v1.point, v2.point))
                self.add_neighborhood(v1, v2)

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
