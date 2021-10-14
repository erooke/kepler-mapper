""" Adapt Mapper format into other common formats.

    - networkx
    - hypernetx
"""
from itertools import combinations


def to_networkx(graph):
    """Convert a Mapper 1-complex to a networkx graph.

    Parameters
    -----------

    graph: dictionary, graph object returned from `kmapper.map`

    Returns
    --------

    g: graph as networkx.Graph() object

    """

    # import here so networkx is not always required.
    import networkx as nx

    simplices = graph["simplices"]

    nodes = simplices[0] if len(simplices) >= 1 else list()
    edges = simplices[1] if len(simplices) >= 2 else list()

    g = nx.Graph()
    g.add_nodes_from(nodes)
    nx.set_node_attributes(g, dict(graph["nodes"]), "membership")

    g.add_edges_from(edges)

    return g


to_nx = to_networkx


def to_hypernetx(graph):
    import hypernetx as hnx

    simplices = graph["simplices"].copy()

    simplices[0] = [(x,) for x in simplices[0]]

    simplices = [set([frozenset(y) for y in x]) for x in simplices]

    result = set()

    # To simplify our hypergraph we first add our top dimensional simplex
    # then remove any faces of that simplex from the simplicial complex
    # this results in a simple hypergraph for which no edge is contained in
    # another
    for S in reversed(simplices):
        for simplex in S:
            result.add(simplex)
            for i in range(1, len(simplex)):
                for edge in map(frozenset, combinations(simplex, i)):
                    simplices[i - 1].discard(edge)

    return hnx.Hypergraph(result)


to_hnx = to_hypernetx
