import project
from objects import S
from funcs import P
from nose.tools import assert_equals
from funcs import Vector as V

def test_adding_4_open_sides_will_not_span_a_wall():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(1, 1, 0)))
    proj.add_segment(S(P(1, 1, 0), P(0, 1, 0)))
    proj.add_segment(S(P(0, 1, 0), P(0, 4, 0)))

    assert_equals(len(proj.walls), 0)

def test_adding_4_sides_will_create_a_wall():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(1, 1, 0)))
    proj.add_segment(S(P(1, 1, 0), P(0, 1, 0)))
    proj.add_segment(S(P(0, 1, 0), P(0, 0, 0)))

    assert_equals(len(proj.walls), 1)

    assert_equals(proj.walls[0].normal(), V(0, 0, 1))

def test_adding_2_sides_will_not_create_a_wall():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(0, 0, 0)))

    assert_equals(len(proj.walls), 0)

