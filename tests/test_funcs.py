import funcs
from funcs import P
from objects import S
from nose.tools import assert_equals

def test_segment_segment_intersection():
    assert_equals(
        funcs.segment_segment_intersection(
            S(P(0, 0, 0), P(1, 0, 0)),
            S(P(1, 0, 1), P(0, 1, 0))),
        None)
