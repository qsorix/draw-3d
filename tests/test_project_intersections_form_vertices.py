import project
from objects import S
from funcs import P
from nose.tools import assert_equals
from funcs import Vector as V

def test_adding_intersecting_segments_creates_vertices():
    proj = project.Project()
    proj.add_segment(S(P(-1, 0,  0), P(1, 0, 0)))
    proj.add_segment(S(P(0, -1,  0), P(0, 1, 0)))

    assert_equals(len(proj.vertices), 5)
    v = proj.get_vertex(P(0,0,0))
    assert v
    assert_equals(len(v.neighbors), 4)

    proj.add_segment(S(P(0,  0, -1), P(0, 0, 1)))
    assert_equals(len(proj.vertices), 7)
    assert_equals(len(v.neighbors), 6)

def test_adding_intersecting_segments_splits_segments():
    proj = project.Project()
    proj.add_segment(S(P(-1, 0,  0), P(1, 0, 0)))
    proj.add_segment(S(P(0, -1,  0), P(0, 1, 0)))

    assert_equals(len(proj.segments), 4)
