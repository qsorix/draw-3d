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

def test_incident_edges_rotate_clockwise_2():
    #Looking for insertion point at vertex  (16, -1, 0)
    #  existing neighbors:
    #     Vx(10, 0, 0)
    #     Vx(15, 4, 0)
    #  point to add (20, -1, 0)
    p0 = P(16, -1, 0)
    p1 = P(10, 0, 0)
    p2 = P(15, 4, 0)

    p3 = P(20, -1, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    a.add_segment(S(p0, p1))
    a.add_segment(S(p0, p2))
    a.add_segment(S(p0, p3))
    v0 = a.get_vertex(p0)
    v1 = a.get_vertex(p1)
    v2 = a.get_vertex(p2)
    v3 = a.get_vertex(p3)

    assert_equals(list(v0.cw_neighbors()), [v1, v2, v3])

def test_incident_edges_rotate_clockwise_3():
    # Looking for insertion point at vertex  (10, 10, 0)
    #   existing neighbors:
    #      Vx(10,0,0)
    #      Vx(0,10,0)
    #   point to add (12, 8, 0)

    p0 = P(10, 10, 0)
    p1 = P(10,  0, 0)
    p2 = P( 0, 10, 0)

    p3 = P(12, 8, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    a.add_segment(S(p0, p1))
    a.add_segment(S(p0, p2))
    a.add_segment(S(p0, p3))
    v0 = a.get_vertex(p0)
    v1 = a.get_vertex(p1)
    v2 = a.get_vertex(p2)
    v3 = a.get_vertex(p3)

    assert_equals(list(v0.cw_neighbors()), [v1, v2, v3])


def test_face_is_formed_from_a_cycle_of_edges():
    p0 = P(0, 0, 0)
    p1 = P(1, 0, 0)
    p2 = P(0, 1, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    a.add_segment(S(p0, p1))
    a.add_segment(S(p1, p2))
    a.add_segment(S(p2, p0))

    v0 = a.get_vertex(p0)
    v1 = a.get_vertex(p1)
    v2 = a.get_vertex(p2)

    assert_equals(v0.degree(), 2)
    assert_equals(v1.degree(), 2)
    assert_equals(v2.degree(), 2)

    print(list(v0.hedge.cycle_vertices()),
                  [v0, v2, v1])
    assert_equals(list(v0.hedge.cycle_vertices()),
                  [v0, v2, v1])
    assert v0.hedge.is_on_proper_cycle()
    assert v0.hedge.is_on_clockwise_cycle()

    assert v0.hedge.twin.is_on_proper_cycle()
    assert not v0.hedge.twin.is_on_clockwise_cycle()

    assert v0.hedge.twin.face
    assert_equals(len(a.faces), 1)

def test_face_is_split_when_edge_crosses_existing_face():
    p0 = P(0, 0, 0)
    p1 = P(1, 0, 0)
    p2 = P(1, 1, 0)
    p3 = P(0, 1, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    a.add_segment(S(p0, p1))
    a.add_segment(S(p1, p2))
    a.add_segment(S(p2, p3))
    a.add_segment(S(p3, p0))

    assert_equals(len(a.faces), 1)

    a.add_segment(S(p1, p3))

    assert_equals(len(a.faces), 2)

def test_face_can_have_isolated_vertices():
    p0 = P( 0,  0, 0)
    p1 = P(10,  0, 0)
    p2 = P(10, 10, 0)
    p3 = P( 0, 10, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    a.add_segment(S(p0, p1))
    a.add_segment(S(p1, p2))
    a.add_segment(S(p2, p3))
    a.add_segment(S(p3, p0))

    assert_equals(len(a.faces), 1)

    p5 = P( 2, 2, 0)

    a.add_vertex(p5)

    assert_equals(len(a.faces[0].isolated_vertices), 1)

    v5 = a.get_vertex(p5)

    assert_equals(v5.outer_face, a.faces[0])

def test_isolated_vertices_turn_into_holes_when_edges_are_added():
    p0 = P( 0,  0, 0)
    p1 = P(10,  0, 0)
    p2 = P(10, 10, 0)
    p3 = P( 0, 10, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    a.add_segment(S(p0, p1))
    a.add_segment(S(p1, p2))
    a.add_segment(S(p2, p3))
    a.add_segment(S(p3, p0))

    assert_equals(len(a.faces), 1)

    p5 = P( 2, 2, 0)
    p6 = P( 2, 6, 0)

    a.add_vertex(p5)
    a.add_vertex(p6)

    assert_equals(len(a.faces[0].isolated_vertices), 2)

    a.add_segment(S(p5, p6))
    v5 = a.get_vertex(p5)
    v6 = a.get_vertex(p6)

    assert_equals(len(a.faces[0].isolated_vertices), 0)
    assert_equals(v5.outer_face, None)
    assert_equals(v6.outer_face, None)

    assert_equals(len(a.faces[0].inner_ccbs), 1)

def test_hole_connected_to_its_outer_ccb_is_no_longer_a_hole():
    p0 = P( 0,  0, 0)
    p1 = P(10,  0, 0)
    p2 = P(10, 10, 0)
    p3 = P( 0, 10, 0)

    p5 = P( 2, 2, 0)
    p6 = P( 2, 6, 0)
    p7 = P( 6, 2, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    # add the face
    a.add_segment(S(p0, p1))
    a.add_segment(S(p1, p2))
    a.add_segment(S(p2, p3))
    a.add_segment(S(p3, p0))

    # add the hole
    a.add_segment(S(p5, p6))
    a.add_segment(S(p6, p7))
    a.add_segment(S(p7, p5))

    # check the setup
    assert_equals(len(a.faces), 2)
    assert_equals(len(a.faces[0].inner_ccbs), 1)

    # now add the connecting segment
    a.add_segment(S(p5, p0))

    # hole should be gone
    assert_equals(len(a.faces), 2)
    assert_equals(len(a.faces[0].inner_ccbs), 0)

def test_holes_can_be_surrounded_by_bigger_holes():
    p0 = P( 0,  0, 0)
    p1 = P(10,  0, 0)
    p2 = P(10, 10, 0)

    p3 = P( 2, 1, 0)
    p4 = P( 9, 1, 0)
    p5 = P( 9, 8, 0)

    p6 = P( 4, 2, 0)
    p7 = P( 7, 2, 0)
    p8 = P( 7, 6, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    # order is important, add from the inside
    a.add_segment(S(p6, p7))
    a.add_segment(S(p7, p8))
    a.add_segment(S(p8, p6))

    a.add_segment(S(p3, p4))
    a.add_segment(S(p4, p5))
    a.add_segment(S(p5, p3))

    a.add_segment(S(p0, p1))
    a.add_segment(S(p1, p2))
    a.add_segment(S(p2, p0))

    # we should get 3 faces, 2 of which contain 1 hole each
    print(a.faces)
    print(a.outer_face)
    print("----")
    print(a.faces[1].inner_ccbs)

    assert_equals(len(a.faces), 3)
    assert len(a.faces[0].inner_ccbs) <= 1
    assert len(a.faces[1].inner_ccbs) <= 1
    assert len(a.faces[2].inner_ccbs) <= 1
    assert_equals(len(a.faces[0].inner_ccbs) +
                  len(a.faces[1].inner_ccbs) +
                  len(a.faces[2].inner_ccbs),
                  2)

def test_holes_can_be_surrounded_by_bigger_holes_2():
    p0 = P( 0,  0, 0)
    p1 = P(10,  0, 0)
    p2 = P(10, 10, 0)

    p3 = P( 2, 1, 0)
    p4 = P( 9, 1, 0)
    p5 = P( 9, 8, 0)

    p6 = P( 4, 2, 0)
    p7 = P( 7, 2, 0)
    p8 = P( 7, 6, 0)

    plane = Plane(V(0, 0, 1), p0)
    a = Arrangement(plane)

    # order is important, add from the middle
    a.add_segment(S(p0, p1))
    a.add_segment(S(p1, p2))
    a.add_segment(S(p2, p0))

    a.add_segment(S(p6, p7))
    a.add_segment(S(p7, p8))
    a.add_segment(S(p8, p6))

    a.add_segment(S(p3, p4))
    a.add_segment(S(p4, p5))
    a.add_segment(S(p5, p3))


    # we should get 3 faces, 2 of which contain 1 hole each
    print(a.faces)
    print(a.outer_face)

    assert_equals(len(a.faces), 3)
    assert len(a.faces[0].inner_ccbs) <= 1
    assert len(a.faces[1].inner_ccbs) <= 1
    assert len(a.faces[2].inner_ccbs) <= 1
    assert_equals(len(a.faces[0].inner_ccbs) +
                  len(a.faces[1].inner_ccbs) +
                  len(a.faces[2].inner_ccbs),
                  2)
