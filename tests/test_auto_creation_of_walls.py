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

def test_adding_4_sides_on_different_planes_will_not_create_a_wall():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(1, 0, 1)))
    proj.add_segment(S(P(1, 0, 1), P(0, 1, 0)))
    proj.add_segment(S(P(0, 1, 0), P(0, 0, 0)))

    assert_equals(len(proj.walls), 0)

def test_more_points_on_a_single_face_still_spans_a_wall():
    ps = [P(0, 0, 0),
          P(1, 0, 0),
          P(2, 0, 0),
          P(2, 2, 0),
          P(1, 2, 0),
          P(1, 1, 0),
          P(0, 1, 0)]
    proj = project.Project()
    for i in range(len(ps)):
        proj.add_segment(S(ps[i], ps[(i+1)%len(ps)]))

    assert_equals(len(proj.walls), 1)

def test_wall_is_spawned_when_segments_arrive_out_of_order():
    # check that segments don't need to be oriented in the same (clockwise)
    # direction

    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(0, 1, 0)))
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(1, 1, 0)))

    assert_equals(len(proj.walls), 0)

    proj.add_segment(S(P(0, 1, 0), P(1, 1, 0)))

    assert_equals(len(proj.walls), 1)

def test_two_walls_can_appear_at_once():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(1, 1, 0)))
    proj.add_segment(S(P(1, 1, 0), P(0, 1, 0)))

    proj.add_segment(S(P(0, 0, 0), P(0, 0, 1)))
    proj.add_segment(S(P(0, 0, 1), P(0, 1, 1)))
    proj.add_segment(S(P(0, 1, 1), P(0, 1, 0)))

    assert_equals(len(proj.walls), 0)

    proj.add_segment(S(P(0, 0, 0), P(0, 1, 0)))

    assert_equals(len(proj.walls), 2)
