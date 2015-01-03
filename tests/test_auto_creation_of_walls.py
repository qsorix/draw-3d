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

def _skip_test_two_walls_can_appear_at_once():
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

def test_created_wall_must_include_just_added_segment():
    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(1, 1, 0)))
    print ("###################")
    proj.add_segment(S(P(1, 1, 0), P(0, 0, 0)))
    assert_equals(len(proj.walls), 1)
    proj.walls[:] = []

    proj.add_segment(S(P(-1, 0, 0), P(0, 0, 0)))

    assert_equals(len(proj.walls), 0)

def test_created_walls_are_not_overlapping_other_surfaces():
    # +-----+
    # |xxxxx|
    # |xx+--+
    # |xx|  |
    # +--+--+

    proj = project.Project()
    proj.add_segment(S(P(0, 0, 0), P(1, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(2, 0, 0)))
    proj.add_segment(S(P(1, 0, 0), P(1, 1, 0)))
    proj.add_segment(S(P(2, 0, 0), P(2, 1, 0)))
    proj.add_segment(S(P(1, 1, 0), P(2, 1, 0)))
    assert_equals(len(proj.walls), 1)

    proj.add_segment(S(P(0, 0, 0), P(0, 2, 0)))
    proj.add_segment(S(P(2, 1, 0), P(2, 2, 0)))
    proj.add_segment(S(P(0, 2, 0), P(2, 2, 0)))

    assert_equals(len(proj.walls), 2)
    w = proj.walls[1]
    assert_equals(len(w.vertices), 6)
    print("Nghs of 0,2: ", proj.get_vertex(P(0,2,0)).neighbors)
    assert P(1, 1, 0) in w.vertices
