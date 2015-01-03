import funcs

class Vertex:
    def __init__(self, arrangement, point):
        self.arrangement = arrangement

        self.hedge = None # this hedge comes into this point
        self.point = point

    def __str__(self):
        return "Vx({},{},{})".format(self.point.x,
                                     self.point.y,
                                     self.point.z)
    __repr__  = __str__

    def get_next_this_hedge_would_get(self, he):
        if not self.hedge:
            return he.next

        he_in, he_out = self._pick_insertion_point_cw(he.source().point)
        return he_out

    def add_incident_hedge(self, he):
        assert he.target() == self

        if not self.hedge:
            self.hedge = he
            return

        he_in, he_out = self._pick_insertion_point_cw(he.source().point)

        he_in.next = he.twin
        he.twin.prev = he_in

        he_out.prev = he
        he.next = he_out

    def cw_incident_hedges(self):
        if not self.hedge:
            return
        start = self.hedge
        current = start
        while True:
            yield current
            current = current.next.twin
            if current == start:
                break

    def cw_neighbors(self):
        for he in self.cw_incident_hedges():
            yield he.source()

    def has_in_immediate_neighborhood(self, v):
        for n in self.cw_neighbors():
            if n == v:
                return True
        return False

    def degree(self):
        d = 0
        for v in self.cw_incident_hedges():
            d = d+1
        return d

    def _pick_insertion_point_cw(self, point):
        print ("Looking for insertion point at vertex ", self.point)
        print ("  existing neighbors:")
        for n in self.cw_neighbors():
            print("    ", n)
        print ("  point to add", point)
        if self.degree() == 1:
            return self.hedge, self.hedge.twin

        point_v = funcs.vector_from_to(self.point, point)

        for current in self.cw_incident_hedges():
            next = current.next.twin

            cpoint_v = funcs.vector_from_to(self.point, current.source().point)
            npoint_v = funcs.vector_from_to(self.point, next.source().point)
            print ("  checking if fits between ", cpoint_v, " and ", npoint_v)

            if funcs.rotates_clockwise_3(cpoint_v, point_v, npoint_v,
                                         self.arrangement.plane):
                return current, current.next

        raise Exception("CW insertion point not found for "\
                        "{}".format(point))

class Face:
    def __init__(self, arrangement):
        self.arrangement = arrangement
        self.hedge = None

    def __str__(self):
        if self.hedge:
            return "<Face {}>".format(list(self.hedge.cycle_vertices()))
        else:
            return "<Face ?>"

    __repr__ = __str__

class HE:
    def __init__(self, arrangement):
        self.arrangement = arrangement

        self.face = None
        self.vertex = None
        self.prev = None
        self.next = None
        self.twin = None

    def __str__(self):
        return ("<HE {} to {}>".format(self.source().point,
                                       self.target().point))
    __repr__ = __str__

    def target(self):
        return self.vertex

    def source(self):
        return self.twin.vertex

    def cycle_hedges(self):
        start = self
        current = start
        while True:
            yield current
            current = current.next
            if current == start:
                break

    def cycle_vertices(self):
        for hedge in self.cycle_hedges():
            yield hedge.vertex

    def is_on_proper_cycle(self):
        for he in self.cycle_hedges():
            if he == self.twin:
                return False
        return True

    def is_on_clockwise_cycle(self):
        path_cross = funcs.Vector(0,0,0)
        for he in self.cycle_hedges():
            v1 = funcs.vector_from_to(
                he.source().point,
                he.target().point)
            v2 = funcs.vector_from_to(
                he.next.source().point,
                he.next.target().point)
            path_cross = funcs.add_vectors(path_cross,
                                           funcs.cross(v1, v2))

        path_cross = funcs.unit(path_cross)
        normal = funcs.unit(self.arrangement.plane.normal)
        return path_cross != normal


def make_halfedge_twins(arrangement, v1, v2):
    he1 = HE(arrangement)
    he2 = HE(arrangement)

    he1.vertex = v1
    he1.twin = he2
    he1.next = he2
    he1.prev = he2

    he2.vertex = v2
    he2.twin = he1
    he2.next = he1
    he2.prev = he1

    return he1, he2

class Arrangement:
    def __init__(self, plane):
        self.plane = plane
        self.vertices = []
        self.faces = []

    def add_vertex(self, point):
        v = self.get_vertex(point)
        if v:
            return v
        v = Vertex(self, point)
        self.vertices.append(v)
        # TODO: set face? or add this point to a face?
        return v

    def get_vertex(self, point):
        for v in self.vertices:
            if v.point == point:
                return v
        return None

    def add_segment(self, s):
        v1 = self.add_vertex(s.a)
        v2 = self.add_vertex(s.b)

        if self._has_hedges_between(v1, v2):
            return

        he1, he2 = make_halfedge_twins(self, v1, v2)

        # set these two before adding the edges
        split_new_face = True or False
        is_split_face_contained = True or False

        he1_next_face = v1.get_next_this_hedge_would_get(he1).face
        he2_next_face = v2.get_next_this_hedge_would_get(he2).face

        if he1_next_face and he1_next_face == he2_next_face:
            self._remove_face(he1_next_face)

        self._span_hedges_between(v1, v2, he1, he2)

        if he1.is_on_proper_cycle():
            if not he1.is_on_clockwise_cycle():
                self._create_new_face_inside(he1)
        if he2.is_on_proper_cycle():
            if not he2.is_on_clockwise_cycle():
                self._create_new_face_inside(he2)

    def _remove_face(self, face):
        self.faces.remove(face)
        for e in face.hedge.cycle_hedges():
            e.face = None

    def _create_new_face_inside(self, he):
        face = Face(self)
        face.hedge = he

        for e in he.cycle_hedges():
            e.face = face

        self.faces.append(face)

    def _has_hedges_between(self, v1, v2):
        return v1.has_in_immediate_neighborhood(v2)

    def _span_hedges_between(self, v1, v2, he1, he2):
        v1.add_incident_hedge(he1)
        v2.add_incident_hedge(he2)
