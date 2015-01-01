import project
from objects import S
from funcs import P
from nose.tools import assert_equals
from funcs import Vector as V

def test_clockwise_sorted():
    p = project.Project()
    center = p.add_vertex(P(0, 0, 0))
    p1 = p.add_vertex(P(1, 0, 0))
    p2 = p.add_vertex(P(1, 1, 0))
    p3 = p.add_vertex(P(0, 1, 0))
    p4 = p.add_vertex(P(-1, 1, 0))
    p5 = p.add_vertex(P(-1, 0, 0))
    p6 = p.add_vertex(P(-1, -1, 0))
    p7 = p.add_vertex(P(0, -1, 0))
    p8 = p.add_vertex(P(1, -1, 0))

    randomized = [p3, p5, p2, p6, p1, p4, p8, p7]
    expected = [p6, p5, p4, p3, p2, p1, p8, p7]
    result = project.clockwise_sorted(center, randomized, V(0, 0, 1))

    assert_equals (result, expected)



