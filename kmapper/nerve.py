import itertools
import math
from collections import defaultdict
from typing import Optional, Union

__all__ = ["GraphNerve", "SimplicialNerve"]


class Nerve:
    """Base class for implementations of a nerve finder to build a Mapper complex."""

    def __init__(self):
        pass

    def compute(self, nodes, links):
        raise NotImplementedError()


class SimplicialNerve(Nerve):
    """Creates the k-skeleton of the Mapper complex.

    Parameters
    -----------

    min_intersection: int, default is 1
        Minimum intersection considered when computing the nerve. A face will
        be created only when the intersection between nodes is greater than or
        equal to `min_intersection`

    dim: Optional[int], default is None
        The dimension of the simplicial complex to generate. If `dim = k` then
        the `k` skeleton of the nerve is returned. If `dim = None` then the
        entire simplicial complex is computed.
    """

    def __init__(self, min_intersection=1, dim: Optional[int] = None):
        if min_intersection <= 0:
            raise ValueError("Minimum intersection must be a positive integer")

        if dim and dim < 0:
            raise ValueError("Dimension must be non-negative")

        self.min_intersection = min_intersection
        self.dim: Optional[int] = dim

    def __repr__(self):
        return "SimplicialNerve(min_intersection={}, dim={})".format(
            self.min_intersection, self.dim
        )

    def compute(self, nodes):
        """Helper function to find edges of the overlapping clusters.

        Parameters
        ----------
        nodes:
            A dictionary with entires `{node id}:{list of ids in node}`

        Returns
        -------
        edges:
            A 1-skeleton of the nerve (intersecting  nodes)

        simplicies:
            Complete list of simplices

        """

        simplices = [[n] for n in nodes]
        result = defaultdict(list)

        if self.dim == 0:
            return result, simplices

        _nodes = {k: frozenset(v) for k, v in nodes.items()}

        # Currently edges need to be treated seperately to appease the api

        # Create links when clusters from different hypercubes have members with the same sample id.
        candidates = itertools.combinations(_nodes.items(), 2)
        for (key_1, node_1), (key_2, node_2) in candidates:
            # if there are non-unique members in the union
            if len(node_1.intersection(node_2)) >= self.min_intersection:
                result[key_1].append(key_2)
                simplices.append([key_1, key_2])

        dimensions = range(2, self.dim + 1) if self.dim else itertools.count(2)

        for current_dim in dimensions:
            more = False
            candidates = itertools.combinations(_nodes.items(), current_dim + 1)

            for candidate in candidates:
                key, elements = zip(*candidate)
                if len(frozenset.intersection(*elements)) >= self.min_intersections:
                    simplices.append(list(key))
                    more = True

            if not more:
                # If no k-simplices are found there are no k+1 simplices either
                break

        return result, simplices


class GraphNerve(SimplicialNerve):
    """Creates the 1-skeleton of the Mapper complex.

    Parameters
    -----------

    min_intersection: int, default is 1
        Minimum intersection considered when computing the nerve. An edge will
        be created only when the intersection between two nodes is greater than
        or equal to `min_intersection`

    """

    def __init__(self, min_intersection: int = 1) -> None:
        super().__init__(min_intersection=min_intersection, dim=1)

    def __repr__(self):
        return "GraphNerve(min_intersection={})".format(self.min_intersection)
