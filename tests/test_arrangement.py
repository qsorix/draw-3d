from nose.tools import assert_equals
from arrangement import Arrangement
import funcs 
from funcs import Vector as V
from funcs import P
from funcs import Plane
from objects import S

def test_incident_edges_rotate_clockwise():
    p0 = P(0, 0, 0)
    p1 = P(1, 0, 0)
    p2 = P(0, -1, 0)
    p3 = P(-1, 0, 0)
    p4 = P(0, 1, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    a.add_segment(S(p0, p1))
    a.add_segment(S(p0, p2))
    a.add_segment(S(p0, p3))
    a.add_segment(S(p0, p4))

    v0 = a.get_vertex(p0)
    v1 = a.get_vertex(p1)
    v2 = a.get_vertex(p2)
    v3 = a.get_vertex(p3)
    v4 = a.get_vertex(p4)

    assert_equals(v0.degree(), 4)
    assert_equals(v0.point, p0)

    assert_equals(list(v0.cw_neighbors()), [v1, v2, v3, v4])
