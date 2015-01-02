import project
from objects import S
from funcs import P
from nose.tools import assert_equals

def test_adding_segment_introduces_vertices_from_endpoints():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))

    assert_equals(len(proj.vertices), 2)

def test_existing_vertices_are_not_duplicated():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(1, 1, 0)))

    assert_equals(len(proj.vertices), 3)

def test_vertices_form_a_graph_based_on_segments():
    proj = project.Project()
    p1 = P(0, 0, 0)
    p2 = P(1, 0, 0)
    p3 = P(1, 1, 0)
    proj.add_segment(S(p1, p2))
    proj.add_segment(S(p2, p3))

    v1 = proj.get_vertex(p1)
    assert_equals(len(v1.neighbors), 1)

    v2 = proj.get_vertex(p2)
    assert_equals(len(v2.neighbors), 2)

    v3 = proj.get_vertex(p3)
    assert_equals(len(v3.neighbors), 1)

    assert v2 in v1.neighbors
    assert v2 in v3.neighbors
    assert v1 in v2.neighbors
    assert v3 in v2.neighbors
