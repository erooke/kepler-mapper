import pytest

from kmapper import GraphNerve


class TestNerve:
    def test_graphnerve(self):
        nerve = GraphNerve()

        groups = {"a": [1, 2, 3, 4], "b": [1, 2, 5], "c": [5, 6, 7]}
        simplices = nerve.compute(groups)

        # all vertices are simplices
        assert all([k in simplices[0] for k in groups])
        edges = set([frozenset(edge) for edge in simplices[1]])

        # graph should be a -- b -- c
        expected = set([frozenset(edge) for edge in [["a", "b"], ["b", "c"]]])
        assert edges == expected

    def test_simplices(self):
        nerve = GraphNerve()
        groups = {"a": [1, 2, 3, 4], "b": [1, 2, 5], "c": [1, 5, 6, 7]}
        simplices = nerve.compute(groups)
        assert len(simplices[0]) == 3
        assert len(simplices[1]) == 3
        assert {"a", "b"} in map(set, simplices[1])
        assert len(simplices) == 2

    def test_min_intersection(self):
        nerve = GraphNerve(min_intersection=2)

        groups = {"a": [1, 2, 3, 4], "b": [1, 2, 5], "c": [5, 6, 7]}
        simplices = nerve.compute(groups)

        # all vertices are simplices
        assert all([k in simplices[0] for k in groups])
        edges = set([frozenset(edge) for edge in simplices[1]])

        # graph should be a -- b    c
        expected = {frozenset(["a", "b"])}
        assert edges == expected

    def test_finds_a_link(self):
        nerve = GraphNerve()
        groups = {"a": [1, 2, 3, 4], "b": [1, 2, 3, 4]}
        simplices = nerve.compute(groups)

        assert ("a", "b") in simplices[1] or ("b", "a") in simplices[1]

    def test_no_link(self):
        nerve = GraphNerve()
        groups = {"a": [1, 2, 3, 4], "b": [5, 6, 7]}

        simplices = nerve.compute(groups)
        assert not simplices[1]

    def test_pass_through_result(self):
        nerve = GraphNerve()
        groups = {"a": [1], "b": [2]}

        simplices = nerve.compute(groups)
        assert not simplices[1]
