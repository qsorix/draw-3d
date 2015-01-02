import project
from objects import S
from funcs import P
from nose.tools import assert_equals
from funcs import Vector as V

def test_adding_intersecting_segments_creates_vertices():
    pc = P(0, 0, 0)
    p1 = P(-1, 0,  0)
    p2 = P(1, 0, 0)
    p3 = P(0, -1,  0)
    p4 = P(0, 1, 0)
    p5 = P(0, 0, -1)
    p6 = P(0, 0, 1)
    proj = project.Project()
    proj.add_segment(S(p1, p2))
    proj.add_segment(S(p3, p4))
    proj.add_segment(S(p5, p6))

    v = proj.get_vertex(pc)
    assert_equals(len(proj.vertices), 7)
    assert_equals(len(v.neighbors), 6)

    for p in [p1, p2, p3, p4, p5, p6]:
        v = proj.get_vertex(p)
        print (v)
        assert_equals(len(v.neighbors), 1)

def test_adding_segment_with_intersection_at_the_end():
    p1, p2 = P(0, 0, 0), P(2, 0, 0)
    p3, p4 = P(1, 1, 0), P(1, 0, 0)
    proj = project.Project()
    proj.add_segment(S(p1, p2))
    proj.add_segment(S(p3, p4))

    assert_equals(len(proj.vertices), 4)
    assert_equals(len(proj.segments), 3)

def test_adding_intersecting_segments_creates_vertices_with_proper_neighborhood():
    p1 = P(0, 0, 0)
    p2 = P(3, 0, 0)
    p3 = P(2, 0, 0)
    p4 = P(2, 2, 0)
    p5 = P(1, 0, 0)
    p6 = P(3, 2, 0)
    proj = project.Project()
    proj.add_segment(S(p1, p2))
    proj.add_segment(S(p3, p4))
    proj.add_segment(S(p5, p6))
    v5 = proj.get_vertex(p5)
    assert_equals(len(v5.neighbors), 3)

def test_adding_intersecting_segments_splits_segments():
    proj = project.Project()
    proj.add_segment(S(P(-1, 0,  0), P(1, 0, 0)))
    proj.add_segment(S(P(0, -1,  0), P(0, 1, 0)))

    assert_equals(len(proj.segments), 4)

def test_removing_segments_remove_vertices():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    assert_equals(len(proj.vertices), 2)
    proj.del_segment(S(P(1, 0, 0), P(0, 0, 0)))
    assert_equals(len(proj.segments), 0)
    assert_equals(len(proj.vertices), 0)

def test_removing_segments_remove_disjoint_vertices():
    p1 = P(0, 0, 0)
    p2 = P(1, 0, 0)
    p3 = P(0, 1, 0)

    proj = project.Project()
    proj.add_segment(S(p1, p2))
    proj.add_segment(S(p1, p3))
    assert_equals(len(proj.vertices), 3)

    proj.del_segment(S(p3, p1))
    assert_equals(len(proj.segments), 1)

    v1 = proj.get_vertex(p1)
    v2 = proj.get_vertex(p2)

    assert_equals(len(v1.neighbors), 1)
    assert_equals(len(v2.neighbors), 1)

    assert_equals(len(proj.vertices), 2)

def test_removing_segments_can_simplify_previously_intersected_segment():
    p1, p2 = P(-1, 0, 0),  P(1, 0, 0)
    p3, p4 = P(0,  0, 0),  P(0, 1, 0)
    proj = project.Project()
    proj.add_segment(S(p1, p2))
    proj.add_segment(S(p3, p4))

    proj.del_segment(S(p3, p4))
    assert_equals(len(proj.segments), 1)
    assert_equals(len(proj.vertices), 2)
